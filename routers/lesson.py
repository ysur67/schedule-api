from datetime import date
from typing import Iterable, Optional

from core.dependencies import get_db
from core.schemas.lesson import Lesson
from core.service.lesson import get_lessons
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/lessons/", response_model=Iterable[Lesson])
async def get_lessons_view(date: Optional[date], db: AsyncSession = Depends(get_db)):
    return await get_lessons(db, date=date)
