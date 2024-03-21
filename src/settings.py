from enum import StrEnum, auto
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

__all__ = [
    "Environment",
    "settings",
]


class Environment(StrEnum):
    DEV = auto()
    PROD = auto()


LoggingLevel = Literal[
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARNING",
    "WARN",
    "INFO",
    "DEBUG",
    "NOTSET",
]


class Settings(BaseSettings):
    """Global application settings loaded from the .env file."""

    env: Environment = Environment.DEV
    logger_name: str = "project_logger"
    logging_level: LoggingLevel = "INFO"


load_dotenv(override=True)
settings = Settings()
