from pathlib import Path
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_NAME: str
    TEST_DB_PASS: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: str

    YOUTUBE_LANGUAGE: str = "ru"

    STORAGE_PATH: Path

    GENIUS_CLIENT_ACCESS_TOKEN: Optional[str]

    @property
    def DATABASE_URL(self):
        return (
            "postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def TEST_DATABASE_URL(self):
        return (
            "postgresql+asyncpg://"
            f"{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:"
            f"{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

    MODE: Literal["DEV", "TEST", "PROD"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

settings.STORAGE_PATH.mkdir(exist_ok=True)
