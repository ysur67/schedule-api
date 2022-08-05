from core.models.mixins import IsActiveMixin, TitleMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class EducationalLevel(TitleMixin, IsActiveMixin):
    __tablename__ = "educational_level"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True)
    groups = relationship("Group", back_populates="level")

    __mapper_args__ = {
        "polymorphic_identity": "educational_level",
    }


class Group(TitleMixin, IsActiveMixin):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(
        Integer,
        ForeignKey("educational_level.id", ondelete="CASCADE")
    )
    level = relationship("EducationalLevel", back_populates="groups")

    lessons = relationship("Lesson", back_populates="group")

    __mapper_args__ = {
        "polymorphic_identity": "group",
    }
