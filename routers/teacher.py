from typing import Iterable

from core.dependencies import get_db
from core.schemas.teacher import Teacher
from core.service.teacher import get_all_teachers
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/teachers/", response_model=Iterable[Teacher])
async def get_all_teacher_view(db: AsyncSession = Depends(get_db)):
    return await get_all_teachers(db)
