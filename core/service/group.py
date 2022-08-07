from typing import Coroutine, Optional

from core.models import EducationalLevel, Group
from core.schemas.group import CreateEducationalLevelSchema, CreateGroupSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_educational_level_by_title(
    db: AsyncSession,
    title: str
) -> Coroutine[Optional[EducationalLevel]]:
    query = select(EducationalLevel).where(EducationalLevel.title == title)
    result = await db.execute(query)
    return result.fetchone()


async def get_group_by_title(db: AsyncSession, title: str) -> Coroutine[Optional[Group]]:
    query = select(Group).where(Group.title == title)
    result = await db.execute(query)
    return result.fetchone()


async def create_educational_level(
    db: AsyncSession,
    level: CreateEducationalLevelSchema
) -> Coroutine[EducationalLevel]:
    result = EducationalLevel(
        title=level.title,
        code=level.code
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


async def create_group(
    db: AsyncSession,
    group: CreateGroupSchema,
) -> Group:
    result = Group(
        title=group.title,
        level=group.level,
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result
