from typing import Coroutine, Optional

from core.models import Classroom
from core.schemas.classroom import CreateClassroomSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_classroom_by_name(db: AsyncSession, title: str) -> Optional[Classroom]:
    query = select(Classroom).where(Classroom.title == title)
    result = await db.execute(query)
    return result.scalar()


async def create_classroom(db: AsyncSession, classroom: CreateClassroomSchema) -> Classroom:
    result = Classroom(
        title=classroom.title,
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result
