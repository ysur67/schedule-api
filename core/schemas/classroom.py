from pydantic import BaseModel


class BaseClassroom(BaseModel):
    id: int | None
    title: str

    class Config:
        orm_mode = True


class CreateClassroomSchema(BaseClassroom):
    pass
