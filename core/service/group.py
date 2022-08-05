from typing import Optional

from core.models import EducationalLevel, Group
from core.structure.group import (CreateEducationalLevelSchema,
                                  CreateGroupSchema)
from sqlalchemy.orm import Session


def get_educational_level_by_title(
    db: Session,
    title: str
) -> Optional[EducationalLevel]:
    return db.query(EducationalLevel).filter(EducationalLevel.title == title).first()


def get_group_by_title(db: Session, title: str) -> Optional[Group]:
    return db.query(Group).filter(Group.title == title).first()


def create_educational_level(
    db: Session,
    level: CreateEducationalLevelSchema
) -> EducationalLevel:
    result = EducationalLevel(
        title=level.title,
        code=level.code
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def create_group(
    db: Session,
    group: CreateGroupSchema,
) -> Group:
    result = Group(
        title=group.title,
        level=group.level,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
