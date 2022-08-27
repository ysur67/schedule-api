from datetime import date
from typing import Iterable, Optional

from core.dependencies import get_db
from core.schemas.lesson import Lesson
from core.service.lesson import (get_lesson_by_id, get_lessons,
                                 get_lessons_by_date_range)
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/lessons/", response_model=Iterable[Lesson])
async def get_lessons_view(date: Optional[date], db: AsyncSession = Depends(get_db)):
    return await get_lessons(db, date=date)


@router.get("/lessons/{id}/", response_model=Lesson)
async def get_lesson_by_id_view(id: int, db: AsyncSession = Depends(get_db)):
    return await get_lesson_by_id(db, id_=id)


@router.get("/lessons-by-date-range/", response_model=Iterable[Lesson])
async def get_lessons_by_date_range_view(
    date_start: date,
    date_end: date,
    db: AsyncSession = Depends(get_db)
):
    return await get_lessons_by_date_range(
        db=db,
        date_start=date_start,
        date_end=date_end,
    )
