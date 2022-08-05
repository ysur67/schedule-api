from core.models.mixins import IsActiveMixin, TitleMixin
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship


class Subject(TitleMixin, IsActiveMixin):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True, index=True)

    lessons = relationship("Lesson", back_populates="subject")

    __mapper_args__ = {
        "polymorphic_identity": "subject",
    }
