from typing import Coroutine, Optional

from core.models import Subject
from core.schemas.subject import CreateSubjectSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_subject_by_title(db: AsyncSession, title: str) -> Coroutine[Optional[Subject]]:
    query = select(Subject).where(Subject.title == title)
    result = await db.execute(query)
    return result.fetchone()


async def create_subject(db: AsyncSession, subject: CreateSubjectSchema) -> Coroutine[Subject]:
    result = Subject(
        title=subject.title
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result
