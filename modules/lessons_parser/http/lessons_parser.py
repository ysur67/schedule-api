from datetime import date, datetime, time
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from core.database import Base
from core.dependencies import get_db
from core.models import Classroom, Group, Lesson, Subject, Teacher
from core.schemas.classroom import CreateClassroomSchema
from core.schemas.group import CreateGroupSchema
from core.schemas.lesson import CreateLessonSchema, GetLessonSchema
from core.schemas.subject import CreateSubjectSchema
from core.schemas.teacher import CreateTeacherSchema
from core.service.classroom import create_classroom, get_classroom_by_name
from core.service.group import create_group, get_group_by_title
from core.service.lesson import (create_lesson, get_lesson_by_params,
                                 update_lesson)
from core.service.subject import create_subject, get_subject_by_title
from core.service.teacher import create_teacher, get_teacher_by_name
from fastapi import Depends
from modules.lessons_parser.utils import (get_date_from_string,
                                          get_time_range_from_string,
                                          get_url_from_string)
from sqlalchemy.orm import Session

from .base import BaseHttpParser, Counter


class LessonsParser(BaseHttpParser):
    logging_name: str = "Main Site Parser"

    def __init__(self, url: str, payload_data: Dict, db: Session) -> None:
        super().__init__(url, payload_data)
        self.db = db
        self.lessons_counter = Counter(name='lessons')
        self.groups_counter = Counter(name='groups')
        self.classrooms_counter = Counter(name='classrooms')
        self.subject_counter = Counter(name='subjects')
        self.teachers_counter = Counter(name='teachers')

    def on_set_up(self):
        super().on_set_up()
        self.logger.info("Начинается парсинг занятий...")
        self.logger.info("Полученный адрес: %s", self.url)
        self.logger.info("Поля запроса: %s", self.payload_data)

    def parse(self):
        date_titles: List[BeautifulSoup] = self.soup.find_all("h4")
        print(date_titles)
        for title in date_titles:
            parent_center = title.parent
            table = parent_center.next_sibling
            if table.name != "table":
                self.logger.error("Не была найдена таблица")
                continue
            lesson_date = get_date_from_string(title.get_text())
            self.parse_table(table, lesson_date)
        self.logger.info('Teachers created: %d', self.teachers_counter.created)
        self.logger.info('Teachers found in local db: %d',
                         self.teachers_counter.updated)
        self.logger.info('Groups created: %d', self.groups_counter.created)
        self.logger.info('Groups found in local db: %d',
                         self.groups_counter.updated)
        self.logger.info('Classrooms created: %d',
                         self.classrooms_counter.created)
        self.logger.info('Classrooms found in local db: %d',
                         self.classrooms_counter.updated)
        self.logger.info('Subjects created: %d', self.subject_counter.created)
        self.logger.info('Subjects found in local db: %d',
                         self.subject_counter.updated)
        self.logger.info('Lessons created: %d', self.lessons_counter.created)
        self.logger.info('Lessons found in local db: %d',
                         self.lessons_counter.updated)

    def parse_table(self, table: BeautifulSoup, lesson_date: date) -> None:
        rows = table.find_all("tr")
        if not rows:
            return self.logger.error("Таблица не содержит строк!")
        # Удаляем первую строку из таблицы - это хедер
        rows.pop(0)
        _ = self.get_lessons_from_rows(rows, lesson_date)

    def get_lessons_from_rows(self, rows: BeautifulSoup, lesson_date: date) -> List[Lesson]:
        result = []
        for row in rows:
            lesson = self.get_lessons_from_single_row(row, lesson_date)
            if lesson:
                result.append(lesson)
        return result

    def get_lessons_from_single_row(self, row: BeautifulSoup, lesson_date: date) -> List[Lesson]:
        tds = row.find_all("td")
        if not tds:
            return self.logger.error("Строка не содержит значений, пропуск...")
        # Удаляем первый элемент - это номер строки
        tds.pop(0)
        # TODO: Вот с этим уродском, если возможно - что-то придумать
        for index, cell in enumerate(tds):
            if index == 0:
                groups = self.parse_groups(cell)
            elif index == 1:
                time_start, time_end = get_time_range_from_string(
                    cell.get_text()
                )
            elif index == 2:
                classroom = self.parse_classroom(cell)
            elif index == 3:
                subject, href = self.parse_subject(cell)
            elif index == 4:
                teacher = self.parse_teacher(cell)
            elif index == 5:
                note = self.parse_note(cell)
        if subject is None:
            return None
        result = []
        for group in groups:
            lesson = self.parse_lesson(
                group=group,
                lesson_date=lesson_date,
                time_start=time_start,
                time_end=time_end,
                classroom=classroom,
                subject=subject,
                teacher=teacher,
                note=note,
                href=href
            )
            result.append(lesson)
        return result

    def parse_groups(self, group: BeautifulSoup) -> List[Group]:
        groups_titles = self.get_title(group)
        result = []
        # Группы могут быть написаны следующим образом
        # 112, 1-И
        # Поэтому необходимо делить строку по запятой
        for title in groups_titles.split(","):
            group_obj = get_group_by_title(db=self.db, title=title)
            if group_obj:
                self.groups_counter.append_updated()
                self.log_operation(group_obj, "найдена")
                result.append(group_obj)
                continue
            group_obj = create_group(
                db=self.db,
                group=CreateGroupSchema(
                    title=title,
                )
            )
            self.groups_counter.append_created()
            self.log_operation(group_obj, "создана")
            result.append(group_obj)
        return result

    def parse_classroom(self, classroom: BeautifulSoup) -> Classroom:
        title = self.get_title(classroom, raise_exception=False)
        if not title:
            return self.logger.error("У записи не имеется аудитории!")
        result = get_classroom_by_name(
            db=self.db,
            title=title
        )
        if result:
            self.classrooms_counter.append_updated()
            self.log_operation(result, "найдена")
            return result
        result = create_classroom(
            db=self.db,
            classroom=CreateClassroomSchema(title=title)
        )
        self.classrooms_counter.append_created()
        self.log_operation(result, "создана")
        return result

    def parse_subject(self, subject: BeautifulSoup) -> 'tuple[Subject, Optional[str]]':
        title = self.get_title(subject, raise_exception=False)
        if title is None:
            return None, None
        href = get_url_from_string(title)
        if href is not None:
            title = title.replace(href, '')
            title = title.strip()
        result = get_subject_by_title(
            db=self.db,
            title=title
        )
        if result:
            self.log_operation(result, "обновлена")
            self.subject_counter.append_updated()
            return result, href
        result = create_subject(
            db=self.db,
            subject=CreateSubjectSchema(
                title=title,
            )
        )
        self.subject_counter.append_created()
        self.log_operation(result, "создана")
        return result, href

    def parse_teacher(self, teacher: BeautifulSoup) -> Optional[Teacher]:
        title = self.get_title(teacher, raise_exception=False)
        if title is None:
            self.logger.error(
                "The teacher didn't have name %s, setting default name...",
                teacher
            )
            title = "NO DATA"
        result = get_teacher_by_name(
            db=self.db,
            name=title
        )
        if result:
            self.log_operation(result, "найдена")
            self.teachers_counter.append_updated()
            return result
        result = create_teacher(
            db=self.db,
            teacher=CreateTeacherSchema(name=title)
        )
        self.teachers_counter.append_created()
        self.log_operation(result, "создана")
        return result

    def parse_note(self, note: BeautifulSoup) -> Optional[str]:
        return self.get_title(note, raise_exception=False)

    def parse_lesson(
        self,
        group: Group,
        lesson_date: date,
        time_start: time,
        time_end: time,
        classroom: Classroom,
        subject: Subject,
        teacher: Teacher,
        note: str,
        href: str = None
    ) -> Lesson:
        lesson = get_lesson_by_params(
            db=self.db,
            param=GetLessonSchema(
                group=group,
                time_start=time_start,
                classroom=classroom,
                date=lesson_date,
                subject=subject,
                teacher=teacher,
            )
        )
        if lesson:
            lesson.href = href
            lesson = update_lesson(db=self.db, lesson=lesson)
            self.log_operation(lesson, "обновлена")
            self.lessons_counter.append_updated()
            return lesson
        lesson = create_lesson(
            db=self.db,
            lesson=CreateLessonSchema(
                title=subject.title,
                date=lesson_date,
                time_start=time_start,
                time_end=time_end,
                group=group,
                teacher=teacher,
                note=note,
                subject=subject,
                classroom=classroom,
                href=href,
            ),
        )
        self.lessons_counter.append_created()
        self.log_operation(lesson, "создана")
        return lesson

    def log_operation(self, obj: Base, operation: str = "создана/обновлена") -> None:
        msg = f"Была {operation} запись {type(obj)}\n"
        self.logger.info(msg)
