from datetime import date
from typing import Any, Dict, Iterable, Optional

from core.models import Lesson
from core.models.group import Group
from core.schemas.lesson import CreateLessonSchema, GetLessonSchema
from core.schemas.utils import Range
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload


async def get_lesson_by_params(
    db: AsyncSession,
    param: GetLessonSchema
) -> Optional[Lesson]:
    query = select(Lesson).where(
        Lesson.group_id == param.group.id,
        Lesson.teacher_id == param.teacher.id,
        Lesson.time_start == param.time_start,
        Lesson.date == param.date,
    )
    if param.classroom is not None:
        query = query.where(Lesson.classroom_id == param.classroom.id)
    else:
        query = query.where(Lesson.classroom_id == None)
    if param.subject is not None:
        query = query.where(Lesson.subject_id == param.subject.id)
    else:
        query = query.where(Lesson.subject_id == None)
    result = await db.execute(query)
    return result.scalar()


async def get_lesson_by_id(db: AsyncSession, id_: int) -> Optional[Lesson]:
    query = _get_lessons_query(db).where(Lesson.id == id_)
    result = await db.execute(query)
    return result.scalar()


async def get_lessons(
    db: AsyncSession,
    date: Optional[date] = None,
    group_id: Optional[int] = None
) -> Iterable[Lesson]:
    query = _get_lessons_query(db)
    if date is not None:
        query = query.where(Lesson.date == date)
    if group_id is not None:
        query = query.where(Lesson.group_id == group_id)
    result = await db.execute(query)
    return result.scalars()


async def get_groups_by_date(db: AsyncSession, date_: date) -> Iterable[Group]:
    query = select(Group).join(Lesson)
    query = query.where(Lesson.date == date_).distinct(Group.id)
    result = await db.execute(query)
    return result.scalars()


def _get_lessons_query(db: AsyncSession) -> Any:
    return select(Lesson).options(
        joinedload(Lesson.group),
        joinedload(Lesson.classroom),
        joinedload(Lesson.teacher),
        joinedload(Lesson.subject),
    )


async def create_lesson(db: AsyncSession, lesson: CreateLessonSchema) -> Lesson:
    result = Lesson(
        title=lesson.subject.title if lesson.subject is not None else "",
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
    await db.commit()
    await db.refresh(result)
    return result


async def update_lesson(db: AsyncSession, lesson: Lesson) -> Lesson:
    await db.commit()
    await db.refresh(lesson)
    return lesson
