from core.models.group import EducationalLevel
from pydantic import BaseModel


class EducationalLevelBase(BaseModel):
    id: int | None
    title: str
    code: str

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    id: int | None
    title: str

    class Config:
        orm_mode = True


class CreateEducationalLevelSchema(EducationalLevelBase):
    pass


class CreateGroupSchema(GroupBase):
    level: EducationalLevel | None

    class Config:
        arbitrary_types_allowed = True
