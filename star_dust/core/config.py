import secrets

from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    database_dsn: PostgresDsn = Field(default=...)
    debug: bool = False
    secret_key: str = secrets.token_urlsafe(32)
    access_token_expire_minutes: int = 24 * 60 * 7  # 7 days
    api_v1_str: str = "/api/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
