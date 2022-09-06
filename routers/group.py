from typing import Iterable

from core.dependencies import get_db
from core.schemas.group import EducationalLevelSchema, Group
from core.service.group import (get_all_educational_levels, get_all_groups,
                                get_educational_level_by_id,
                                get_groups_by_level_id)
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/educational-levels/", response_model=Iterable[EducationalLevelSchema])
async def get_all_levels_view(db: AsyncSession = Depends(get_db)):
    return await get_all_educational_levels(db)


@router.get("/educational-levels/{id}/", response_model=EducationalLevelSchema)
async def get_level_view(id_: int, db: AsyncSession = Depends(get_db)):
    level = get_educational_level_by_id(db, id_)
    if level is None:
        raise HTTPException(404, detail="Educational level not found")
    return level


@router.get("/educational-levels/{id}/groups", response_model=Iterable[Group])
async def get_groups_by_educational_level_view(id: int, db: AsyncSession = Depends(get_db)):
    return await get_groups_by_level_id(db, id)


@router.get("/groups/", response_model=Iterable[Group])
async def get_all_groups_view(db: AsyncSession = Depends(get_db)):
    return await get_all_groups(db)
