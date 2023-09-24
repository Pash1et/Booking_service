from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "PROD", "TEST"]

    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default="postgres")
    DB_PASS: str = Field(default="postgres")
    DB_NAME: str = Field(default="postgres")

    TEST_DB_HOST: str = Field(default="localhost")
    TEST_DB_PORT: int = Field(default=5433)
    TEST_DB_USER: str = Field(default="postgres_test")
    TEST_DB_PASS: str = Field(default="postgres_test")
    TEST_DB_NAME: str = Field(default="postgres_test")

    SECRET_KEY: str = Field(default="9e0a6b826077929f9a2357bfc2ec945ceecd1df7aad183524f291592cbd6204d")
    ALGORITHM: str = Field(default="HS526")
    EXPIRE: str = Field(default=30)

    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)

    SMTP_HOST: str = Field(default="smtp.smtp.ru")
    SMTP_PORT: int = Field(default=465)
    SMTP_USER: str = Field(default="user@user.com")
    SMTP_PASS: str = Field(default="UserPassword")

    ADMIN_EMAIL: str = Field(default="admin@admin.com")

    USER: str = Field(default="user")
    ADMIN: str = Field(default="admin")

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def TEST_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}"
            f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
