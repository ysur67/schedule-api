import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):

    BASE_DIR = Path(__file__).resolve().parent.parent

    DATABASE_URL = os.getenv("DATABASE_URL")

    LOGGING_DIR = BASE_DIR / 'logs'

    class Config:
        env_file = ".env"
