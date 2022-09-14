from typing import Any

from core.repositories.classrooms_repository import ClassroomsRepository
from core.schemas.classroom import Classroom, CreateClassroomSchema
from core.service.classroom import create_classroom, get_classroom_by_name
from sqlalchemy.ext.asyncio import AsyncSession


class AlchemyClassroomsRepository(ClassroomsRepository):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__()
        self.db = db

    async def get_classroom_by_name(self, title: str) -> Any:
        return get_classroom_by_name(self.db, title)

    async def create_classroom(self, classroom: CreateClassroomSchema) -> Classroom:
        return create_classroom(self.db, classroom)
