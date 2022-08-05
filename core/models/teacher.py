from core.models.mixins import IsActiveMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Teacher(IsActiveMixin):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    lessons = relationship("Lesson", back_populates="teacher")

    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }
