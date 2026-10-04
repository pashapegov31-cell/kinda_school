from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )
    # TOKENS
    TOKEN_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # ADMIN SEES
    ADMIN_NAME: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    # POSTGRES
    DATABASE_URL: str

    # depedencies
    BACKEND_REPO: Literal["memory", "postgres"] = "memory"


settings = Settings()  # pyright: ignore[reportCallIssue]
