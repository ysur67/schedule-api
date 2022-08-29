from datetime import date
from typing import Dict, Iterable, Optional

from core.dependencies import get_db
from core.schemas.group import Group
from core.schemas.lesson import Lesson, LessonsWithGroupSchema
from core.service.lesson import (get_groups_by_date, get_groups_from_lessons,
                                 get_lesson_by_id, get_lessons,
                                 get_lessons_by_date_range)
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from utils.date_time import date_range

router = APIRouter()


@router.get("/lessons/", response_model=Iterable[Lesson])
async def get_lessons_view(
    date: Optional[date] = None,
    group_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    print(group_id)
    return await get_lessons(db, date=date, group_id=group_id)


@router.get("/lessons/{id}/", response_model=Lesson)
async def get_lesson_by_id_view(id: int, db: AsyncSession = Depends(get_db)):
    return await get_lesson_by_id(db, id_=id)


# TODO: ref
@router.get("/lessons-by-date-range/", response_model=Dict[date, LessonsWithGroupSchema])
async def get_lessons_by_date_range_view(
    date_start: date,
    date_end: date,
    db: AsyncSession = Depends(get_db),
):
    result: Dict[date, LessonsWithGroupSchema] = {}
    for date_ in date_range(date_start, date_end):
        lessons = list(await get_lessons(db, date_))
        groups = list(await get_groups_from_lessons(db, lessons))
        result[date_] = LessonsWithGroupSchema(
            lessons=lessons,
            groups=groups
        )
    return result


@router.get("/groups-by-date-range/", response_model=Dict[date, Iterable[Group]])
async def get_groups_by_date_range_view(
    date_start: date,
    date_end: date,
    db: AsyncSession = Depends(get_db)
):
    return {elem: await get_groups_by_date(db, elem) for elem in date_range(date_start, date_end)}
