from pydantic import BaseModel


class BaseSubject(BaseModel):
    id: int | None
    title: str

    class Config:
        orm_mode = True


class CreateSubjectSchema(BaseSubject):
    pass
