from pathlib import Path


class Settings:

    BASE_DIR = Path(__file__).resolve().parent.parent

    LOGGING_DIR = BASE_DIR / 'logs'
