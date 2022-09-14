

from abc import ABC, abstractmethod

from core.schemas.lesson import CreateLessonSchema, GetLessonSchema, Lesson


class LessonsRepository(ABC):

    @abstractmethod
    async def get_lesson_by_query(
        self,
        query: GetLessonSchema
    ) -> Lesson | None:
        pass

    @abstractmethod
    async def get_lesson_by_id(self, id: int) -> Lesson | None:
        pass

    @abstractmethod
    async def get_all_lessons(self) -> list[Lesson]:
        pass

    @abstractmethod
    async def create_lesson(self, lesson: CreateLessonSchema) -> Lesson:
        pass

    @abstractmethod
    async def update_lesson(self, lesson: Lesson) -> Lesson:
        pass
