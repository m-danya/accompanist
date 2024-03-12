from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: str

    @property
    def DATABASE_URL(self):
        return (
            "postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
