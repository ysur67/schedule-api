from typing import Optional

from core.models import Lesson, classroom
from core.schemas.lesson import CreateLessonSchema, GetLessonSchema
from sqlalchemy.orm import Session


def get_lesson_by_params(db: Session, param: GetLessonSchema) -> Optional[Lesson]:
    query = db.query(Lesson).filter(
        Lesson.group_ip == param.group.id,
        Lesson.time_start == param.time_start,
        Lesson.date == param.date,
        Lesson.teacher == param.teacher.id,
    )
    if param.classroom is not None:
        query = query.filter(Lesson.classroom_id == param.classroom.id)
    else:
        query = query.filter(Lesson.classroom_id == None)
    if param.subject is not None:
        query = query.filter(Lesson.subject_id == param.subject.id)
    else:
        query = query.filter(Lesson.subject_id == None)
    return query.filter()


def create_lesson(db: Session, lesson: CreateLessonSchema) -> Lesson:
    result = Lesson(
        date=lesson.date,
        time_start=lesson.time_start,
        time_end=lesson.time_end,
        group_id=lesson.group.id,
        teacher=lesson.teacher.id,
        note=lesson.note,
        classroom_id=lesson.classroom.id if lesson.classroom else None,
        subject_id=lesson.subject.id,
        href=lesson.href,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
