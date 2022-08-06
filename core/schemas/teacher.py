from pydantic import BaseModel


class BaseTeacher(BaseModel):
    id: int | None
    name: str


class CreateTeacherSchema(BaseTeacher):
    pass
