from typing import Coroutine, Optional

from core.models import Lesson
from core.schemas.lesson import CreateLessonSchema, GetLessonSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_lesson_by_params(
    db: AsyncSession,
    param: GetLessonSchema
) -> Coroutine[Optional[Lesson]]:
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
    return result.fetchone()


async def create_lesson(db: AsyncSession, lesson: CreateLessonSchema) -> Coroutine[Lesson]:
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
    await db.commit()
    await db.refresh(result)
    return result


async def update_lesson(db: AsyncSession, lesson: Lesson) -> Coroutine[Lesson]:
    await db.commit()
    await db.refresh(lesson)
    return lesson
