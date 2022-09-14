from datetime import date, time
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from core.database import Base
from core.di.container import Container
from core.repositories import GroupsRepository
from core.repositories.classrooms_repository import ClassroomsRepository
from core.repositories.lessons_repository import LessonsRepository
from core.repositories.subjects_repository import SubjectsRepository
from core.repositories.teachers_repository import TeachersRepository
from core.schemas.classroom import Classroom, CreateClassroomSchema
from core.schemas.group import CreateGroupSchema, Group
from core.schemas.lesson import CreateLessonSchema, GetLessonSchema, Lesson
from core.schemas.subject import CreateSubjectSchema, Subject
from core.schemas.teacher import CreateTeacherSchema, Teacher
from dependency_injector.wiring import Provide, inject
from modules.lessons_parser.utils import (get_date_from_string,
                                          get_time_range_from_string,
                                          get_url_from_string)

from .http_base import BaseHttpParser, Counter


class LessonsParser(BaseHttpParser):
    logging_name: str = "Main Site Parser"

    @inject
    def __init__(
        self,
        url: str,
        payload_data: Dict,
        groups_repository: GroupsRepository = Provide[Container.groups_repository],
        classrooms_repository: ClassroomsRepository = Provide[Container.classrooms_repository],
        subjects_repository: SubjectsRepository = Provide[Container.subjects_repository],
        teachers_repository: TeachersRepository = Provide[Container.teachers_repository],
        lessons_repository: LessonsRepository = Provide[Container.lessons_repository],
    ) -> None:
        super().__init__(url, payload_data)
        self._groups_repository = groups_repository
        self._classrooms_repository = classrooms_repository
        self._subjects_repository = subjects_repository
        self._teachers_repository = teachers_repository
        self._lessons_repository = lessons_repository
        self.lessons_counter = Counter(name='lessons')
        self.groups_counter = Counter(name='groups')
        self.classrooms_counter = Counter(name='classrooms')
        self.subject_counter = Counter(name='subjects')
        self.teachers_counter = Counter(name='teachers')

    async def on_set_up(self) -> None:
        await super().on_set_up()
        self.logger.info("Начинается парсинг занятий...")
        self.logger.info("Полученный адрес: %s", self.url)
        self.logger.info("Поля запроса: %s", self.payload_data)

    async def parse(self) -> None:
        date_titles: List[BeautifulSoup] = self.soup.find_all("h4")
        for title in date_titles:
            parent_center = title.parent
            table = parent_center.next_sibling
            if table.name != "table":
                self.logger.error("Не была найдена таблица")
                continue
            lesson_date = get_date_from_string(title.get_text())
            await self.parse_table(table, lesson_date)
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

    async def parse_table(self, table: BeautifulSoup, lesson_date: date) -> None:
        rows = table.find_all("tr")
        if not rows:
            return self.logger.error("Таблица не содержит строк!")
        # Удаляем первую строку из таблицы - это хедер
        rows.pop(0)
        _ = await self.get_lessons_from_rows(rows, lesson_date)

    async def get_lessons_from_rows(self, rows: BeautifulSoup, lesson_date: date) -> List[Lesson]:
        result = []
        for row in rows:
            lessons = await self.get_lessons_from_single_row(row, lesson_date)
            if lessons:
                result += lessons
        return result

    async def get_lessons_from_single_row(self, row: BeautifulSoup, lesson_date: date) -> List[Lesson]:
        tds = row.find_all("td")
        if not tds:
            return self.logger.error("Строка не содержит значений, пропуск...")
        # Удаляем первый элемент - это номер строки
        tds.pop(0)
        # TODO: Вот с этим уродском, если возможно - что-то придумать
        for index, cell in enumerate(tds):
            if index == 0:
                groups = await self.parse_groups(cell)
            elif index == 1:
                time_start, time_end = get_time_range_from_string(
                    cell.get_text()
                )
            elif index == 2:
                classroom = await self.parse_classroom(cell)
            elif index == 3:
                subject, href = await self.parse_subject(cell)
            elif index == 4:
                teacher = await self.parse_teacher(cell)
            elif index == 5:
                note = await self.parse_note(cell)
        if subject is None:
            return []
        result = []
        for group in groups:
            lesson = await self.parse_lesson(
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

    async def parse_groups(self, group: BeautifulSoup) -> List[Group]:
        groups_titles = self.get_title(group)
        result = []
        # Группы могут быть написаны следующим образом
        # 112, 1-И
        # Поэтому необходимо делить строку по запятой
        for title in groups_titles.split(","):
            result.append(await self._update_or_create_group(title))
        return result

    async def _update_or_create_group(self, title: str) -> Group:
        group_obj = await self._groups_repository.get_group_by_title(
            title=title
        )
        if group_obj:
            self.groups_counter.append_updated()
            self.log_operation(group_obj, "найдена")
            return group_obj
        group_obj = await self._groups_repository.create_group(
            group=CreateGroupSchema(
                title=title,
            )
        )
        self.groups_counter.append_created()
        self.log_operation(group_obj, "создана")
        return group_obj

    async def parse_classroom(self, classroom: BeautifulSoup) -> Classroom:
        title = self.get_title(classroom, raise_exception=False)
        if not title:
            return self.logger.error("У записи не имеется аудитории!")
        result = await self._classrooms_repository.get_classroom_by_name(
            title=title
        )
        if result:
            self.classrooms_counter.append_updated()
            self.log_operation(result, "найдена")
            return result
        result = await self._classrooms_repository.create_classroom(
            classroom=CreateClassroomSchema(title=title)
        )
        self.classrooms_counter.append_created()
        self.log_operation(result, "создана")
        return result

    async def parse_subject(self, subject: BeautifulSoup) -> tuple[Subject | None, str | None]:
        title = self.get_title(subject, raise_exception=False)
        if title is None:
            return None, None
        href = get_url_from_string(title)
        if href is not None:
            title = title.replace(href, '')
            title = title.strip()
        result = await self._subjects_repository.get_subject_by_title(
            title=title
        )
        if result:
            self.log_operation(result, "обновлена")
            self.subject_counter.append_updated()
            return result, href
        result = await self._subjects_repository.create_subject(
            subject=CreateSubjectSchema(
                title=title,
            )
        )
        self.subject_counter.append_created()
        self.log_operation(result, "создана")
        return result, href

    async def parse_teacher(self, teacher: BeautifulSoup) -> Optional[Teacher]:
        title = self.get_title(teacher, raise_exception=False)
        if title is None:
            self.logger.error(
                "The teacher didn't have name %s, setting default name...",
                teacher
            )
            title = "NO DATA"
        result = await self._teachers_repository.get_teacher_by_name(
            name=title
        )
        if result:
            self.log_operation(result, "найдена")
            self.teachers_counter.append_updated()
            return result
        result = await self._teachers_repository.create_teacher(
            teacher=CreateTeacherSchema(name=title)
        )
        self.teachers_counter.append_created()
        self.log_operation(result, "создана")
        return result

    async def parse_note(self, note: BeautifulSoup) -> Optional[str]:
        return self.get_title(note, raise_exception=False)

    async def parse_lesson(
        self,
        group: Group,
        lesson_date: date,
        time_start: time,
        time_end: time,
        classroom: Classroom,
        subject: Subject,
        teacher: Teacher | None,
        note: str | None,
        href: str = None
    ) -> Lesson:
        lesson = await self._lessons_repository.get_lesson_by_query(
            query=GetLessonSchema(
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
            lesson = await self._lessons_repository.update_lesson(
                lesson=lesson
            )
            self.log_operation(lesson, "обновлена")
            self.lessons_counter.append_updated()
            return lesson
        lesson = await self._lessons_repository.create_lesson(
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
