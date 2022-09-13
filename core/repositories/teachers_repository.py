

from abc import ABC

from core.schemas.teacher import CreateTeacherSchema, Teacher


class TeachersRepository(ABC):

    async def get_teacher_by_name(self, name: str) -> Teacher | None:
        pass

    async def get_all_teachers(self) -> list[Teacher]:
        pass

    async def create_teacher(self, teacher: CreateTeacherSchema) -> Teacher:
        pass
