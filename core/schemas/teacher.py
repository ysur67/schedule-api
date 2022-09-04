from pydantic import BaseModel


class BaseTeacher(BaseModel):
    id: int | None
    name: str


class Teacher(BaseTeacher):
    class Config:
        orm_mode = True


class CreateTeacherSchema(BaseTeacher):
    pass
