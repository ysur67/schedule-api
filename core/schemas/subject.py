from pydantic import BaseModel


class BaseSubject(BaseModel):
    id: int | None
    title: str


class CreateSubjectSchema(BaseModel):
    pass
