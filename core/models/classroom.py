from core.models.mixins import IsActiveMixin, TitleMixin
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship


class Classroom(TitleMixin, IsActiveMixin):
    __tablename__ = "classroom"

    id = Column(Integer, primary_key=True, index=True)

    lessons = relationship("Lesson", back_populates="classroom")

    __mapper_args__ = {
        "polymorphic_identity": "classroom",
    }
