from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE: str

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    ADMIN_EMAIL: str

    USER: str = Field(default="user")
    ADMIN: str = Field(default="admin")

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DATABASE_URL(self):
        user = f"{self.DB_USER}:{self.DB_PASS}"
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql+asyncpg://{user}@{database}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
