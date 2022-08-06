from datetime import date, time

from core.schemas.classroom import BaseClassroom
from core.schemas.group import GroupBase
from core.schemas.subject import BaseSubject
from core.schemas.teacher import BaseTeacher
from pydantic import BaseModel


class BaseLesson(BaseModel):
    id: int | None
    title: str
    date: date
    time_start: time
    time_end: time
    group: GroupBase
    teacher: BaseTeacher
    classroom:  BaseClassroom | None
    subject: BaseSubject | None
    note: str | None
    href: str | None


class GetLessonSchema(BaseLesson):
    pass


class CreateLessonSchema(BaseLesson):
    pass
