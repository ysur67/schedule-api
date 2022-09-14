from core.repositories import SubjectsRepository
from core.schemas.subject import CreateSubjectSchema, Subject
from core.service.subject import create_subject, get_subject_by_title
from sqlalchemy.ext.asyncio import AsyncSession


class AlchemySubjectsRepository(SubjectsRepository):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__()
        self.db = db

    async def get_subject_by_title(self, title: str) -> Subject | None:
        return get_subject_by_title(self.db, title)

    async def create_subject(self, subject: CreateSubjectSchema) -> Subject:
        return create_subject(self.db, subject)
