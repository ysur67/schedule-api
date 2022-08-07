from typing import Coroutine, Optional

from core.models import Teacher
from core.schemas.teacher import CreateTeacherSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_teacher_by_name(db: AsyncSession, name: str) -> Optional[Teacher]:
    query = select(Teacher).where(Teacher.name == name)
    result = await db.execute(query)
    return result.scalar()


async def create_teacher(db: AsyncSession, teacher: CreateTeacherSchema) -> Teacher:
    result = Teacher(
        name=teacher.name
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result
