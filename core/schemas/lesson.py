from datetime import date, time
from typing import Iterable

from core.models.classroom import Classroom
from core.models.group import Group
from core.models.subject import Subject
from core.models.teacher import Teacher
from core.schemas.classroom import BaseClassroom
from core.schemas.group import Group as GroupSchema
from core.schemas.group import GroupBase
from core.schemas.subject import BaseSubject
from core.schemas.teacher import BaseTeacher
from core.schemas.teacher import Teacher as TeacherSchema
from pydantic import BaseModel


class BaseLesson(BaseModel):
    id: int | None
    title: str
    date: date
    time_start: time
    time_end: time
    group: GroupSchema
    teacher: TeacherSchema
    classroom:  BaseClassroom | None
    subject: BaseSubject | None
    note: str | None
    href: str | None


class Lesson(BaseLesson):
    class Config:
        orm_mode = True


class LessonsWithGroupSchema(BaseModel):
    groups: list[GroupSchema]
    lessons: list[Lesson]

    class Config:
        orm_mode = True


class GetLessonSchema(BaseModel):
    group: GroupBase
    teacher: BaseTeacher
    classroom: BaseClassroom | None
    subject: BaseSubject | None
    date: date
    time_start: time


class CreateLessonSchema(BaseLesson):
    group: Group
    teacher: Teacher
    classroom:  Classroom | None
    subject: Subject | None

    class Config:
        arbitrary_types_allowed = True
