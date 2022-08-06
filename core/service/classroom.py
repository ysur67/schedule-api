from typing import Optional

from core.models import Classroom
from core.schemas.classroom import CreateClassroomSchema
from sqlalchemy.orm import Session


def get_classroom_by_name(db: Session, title: str) -> Optional[Classroom]:
    return db.query(Classroom).filter(Classroom.title == title).first()


def create_classroom(db: Session, classroom: CreateClassroomSchema) -> Classroom:
    result = Classroom(
        title=classroom.title,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
