

from abc import ABC

from core.schemas.lesson import CreateLessonSchema, GetLessonSchema, Lesson


class LessonsRepository(ABC):

    async def get_lesson_by_query(
        self,
        query: GetLessonSchema
    ) -> Lesson | None:
        pass

    async def get_lesson_by_title(self, title: str) -> Lesson | None:
        pass

    async def get_all_lessons(self) -> list[Lesson]:
        pass

    async def create_lesson(self, lesson: CreateLessonSchema) -> Lesson:
        pass
