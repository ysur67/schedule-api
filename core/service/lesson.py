from typing import Optional

from core.models import Lesson, classroom
from core.schemas.lesson import BaseLesson, CreateLessonSchema, GetLessonSchema
from sqlalchemy.orm import Session


def get_lesson_by_params(db: Session, param: GetLessonSchema) -> Optional[Lesson]:
    query = db.query(Lesson).filter(
        Lesson.group_id == param.group.id,
        Lesson.teacher_id == param.teacher.id,
        Lesson.time_start == param.time_start,
        Lesson.date == param.date,
    )
    if param.classroom is not None:
        query = query.filter(Lesson.classroom_id == param.classroom.id)
    else:
        query = query.filter(Lesson.classroom_id == None)
    if param.subject is not None:
        query = query.filter(Lesson.subject_id == param.subject.id)
    else:
        query = query.filter(Lesson.subject_id == None)
    return query.first()


def create_lesson(db: Session, lesson: CreateLessonSchema) -> Lesson:
    result = Lesson(
        title=lesson.subject.title,
        date=lesson.date,
        time_start=lesson.time_start,
        time_end=lesson.time_end,
        note=lesson.note,
        href=lesson.href,
        subject=lesson.subject,
        classroom=lesson.classroom,
        group=lesson.group,
        teacher=lesson.teacher
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def update_lesson(db: Session, lesson: Lesson) -> Lesson:
    db.commit()
    db.refresh(lesson)
    return lesson
