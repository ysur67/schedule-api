
from core.repositories.teachers_repository import TeachersRepository
from core.schemas.teacher import CreateTeacherSchema, Teacher
from core.service.teacher import (create_teacher, get_all_teachers,
                                  get_teacher_by_name)
from sqlalchemy.ext.asyncio import AsyncSession


class AlchemyTeachersRepository(TeachersRepository):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__()
        self.db = db

    async def get_teacher_by_name(self, name: str) -> Teacher | None:
        return get_teacher_by_name(self.db, name)

    async def get_all_teachers(self) -> list[Teacher]:
        return get_all_teachers(self.db)

    async def create_teacher(self, teacher: CreateTeacherSchema) -> Teacher:
        return create_teacher(self.db, teacher)
