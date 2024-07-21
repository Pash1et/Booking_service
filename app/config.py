from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    MODE: Literal["DEV", "TEST"] = Field(default="DEV")

    DB_NAME: str = Field(default="postgres")
    DB_USER: str = Field(default="postgres")
    DB_PASS: str = Field(default="postgres")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default="5432")

    SMTP_HOST: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default="465")
    SMTP_USER: str = Field(default="smtp_user")
    SMTP_PASS: str = Field(default="smtp_pass")

    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default="6379")

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def database_url_sync(self):
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    SECRET_KEY: str = Field(default="123")
    ALGORITHM: str = Field(default="HS256")


settings = Settings()
