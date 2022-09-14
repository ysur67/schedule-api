from abc import ABC, abstractmethod

from core.schemas.classroom import Classroom, CreateClassroomSchema


class ClassroomsRepository(ABC):

    @abstractmethod
    async def get_classroom_by_name(self, title: str) -> Classroom | None:
        pass

    @abstractmethod
    async def create_classroom(self, classroom: CreateClassroomSchema) -> Classroom:
        pass
