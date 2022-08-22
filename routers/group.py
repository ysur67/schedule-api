from typing import Iterable

from core.dependencies import get_db
from core.schemas.group import EducationalLevel, Group
from core.service.group import (get_all_educational_levels, get_all_groups,
                                get_groups_by_level_id)
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/educational-levels/", response_model=Iterable[EducationalLevel])
async def get_all_levels_view(db: Session = Depends(get_db)):
    return await get_all_educational_levels(db)


@router.get("/groups/", response_model=Iterable[Group])
async def get_all_groups_view(db: Session = Depends(get_db)):
    return await get_all_groups(db)


@router.get("/groups/{id}/", response_model=Iterable[Group])
async def get_groups_by_level_view(level_id: int, db: Session = Depends(get_db)):
    return await get_groups_by_level_id(db=db, level_id=level_id)
