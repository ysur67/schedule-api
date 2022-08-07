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
    # level_id: int

    class Config:
        orm_mode = True


class CreateEducationalLevelSchema(EducationalLevelBase):
    pass


class CreateGroupSchema(GroupBase):
    level: EducationalLevel

    class Config:
        arbitrary_types_allowed = True
