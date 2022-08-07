from typing import Optional

from core.models import Teacher
from core.schemas.teacher import CreateTeacherSchema
from sqlalchemy.orm import Session


def get_teacher_by_name(db: Session, name: str) -> Optional[Teacher]:
    return db.query(Teacher).filter(Teacher.name == name).first()


def create_teacher(db: Session, teacher: CreateTeacherSchema) -> Teacher:
    result = Teacher(
        name=teacher.name
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
