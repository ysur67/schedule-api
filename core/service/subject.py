from typing import Optional

from core.models import Subject
from core.schemas.subject import CreateSubjectSchema
from sqlalchemy.orm import Session


def get_subject_by_title(db: Session, title: str) -> Optional[Subject]:
    return db.query(Subject).filter(Subject.title == title).first()


def create_subject(db: Session, subject: CreateSubjectSchema) -> Subject:
    result = Subject(
        title=subject.title
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
