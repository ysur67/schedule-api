from core.models.mixins import IsActiveMixin, TitleMixin
from sqlalchemy import Column, Date, Integer, String, Text, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Lesson(TitleMixin, IsActiveMixin):
    __tablename__ = "lesson"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, server_default=func.now(type=Date))
    time_start = Column(
        Time,
        server_default=func.current_timestamp(type_=Time)
    )
    time_end = Column(
        Time,
        server_default=func.current_timestamp(type_=Time)
    )
    group_id = Column(Integer, nullable=False)
    teacher_id = Column(Integer, nullable=False)
    note = Column(Text)
    classroom_id = Column(Integer)
    subject_id = Column(Integer, nullable=False)
    href = Column(String)

    group = relationship("Group", back_populates="lessons")
    teacher = relationship("Teacher", back_populates="lessons")
    classroom = relationship("Classroom", back_populates="lessons")
    subject = relationship("Subject", back_populates="lessons")

    __mapper_args__ = {
        "polymorphic_identity": "lesson",
    }
