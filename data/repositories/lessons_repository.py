from core.repositories.lessons_repository import LessonsRepository
from core.schemas.lesson import CreateLessonSchema, GetLessonSchema, Lesson
from core.service.lesson import (create_lesson, get_lesson_by_id,
                                 get_lesson_by_params, get_lessons)
from sqlalchemy.ext.asyncio import AsyncSession


class AlchemyLessonsRepository(LessonsRepository):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__()
        self.db = db

    async def get_lesson_by_query(
        self,
        query: GetLessonSchema
    ) -> Lesson | None:
        return get_lesson_by_params(query)

    async def get_all_lessons(self) -> list[Lesson]:
        return get_lessons(self.db)

    async def create_lesson(self, lesson: CreateLessonSchema) -> Lesson:
        return create_lesson(self.db, lesson)

    async def get_lesson_by_id(self, id: int) -> Lesson | None:
        return get_lesson_by_id(self.db, id)
