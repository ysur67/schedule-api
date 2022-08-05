from pydantic import BaseModel


class EducationalLevelBase(BaseModel):
    title: str
    code: str

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    title: str
    level_id: int

    class Config:
        orm_mode = True


class CreateEducationalLevelSchema(EducationalLevelBase):
    pass


class CreateGroupSchema(GroupBase):
    level: EducationalLevelBase
