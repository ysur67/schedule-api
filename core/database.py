from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)

Base = declarative_base()


async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
