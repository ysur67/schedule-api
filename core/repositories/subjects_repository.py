


from abc import ABC

from core.schemas.subject import CreateSubjectSchema, Subject


class SubjectsRepository(ABC):

    async def get_subject_by_title(self, title: str) -> Subject | None:
        pass

    async def create_subject(self, subject: CreateSubjectSchema) -> Subject:
        pass
