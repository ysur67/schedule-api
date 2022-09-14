

from abc import ABC, abstractmethod

from core.schemas.teacher import CreateTeacherSchema, Teacher


class TeachersRepository(ABC):

    @abstractmethod
    async def get_teacher_by_name(self, name: str) -> Teacher | None:
        pass

    @abstractmethod
    async def get_all_teachers(self) -> list[Teacher]:
        pass

    @abstractmethod
    async def create_teacher(self, teacher: CreateTeacherSchema) -> Teacher:
        pass
