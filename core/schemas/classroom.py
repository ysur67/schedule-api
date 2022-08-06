from pydantic import BaseModel


class BaseClassroom(BaseModel):
    title: str


class CreateClassroomSchema(BaseClassroom):
    pass
