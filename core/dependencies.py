from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session
from core.settings import Settings


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
