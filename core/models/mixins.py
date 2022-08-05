from core.database import Base
from sqlalchemy import Boolean, Column, String


class IsActiveMixin(Base):
    __abstract__ = True

    is_active = Column(Boolean, default=False)


class TitleMixin(Base):
    __abstract__ = True

    title = Column(String)
