import secrets
from typing import Any, Dict, Optional

from pydantic import BaseSettings, EmailStr, Field, PostgresDsn, validator


class Settings(BaseSettings):
    database_dsn: PostgresDsn = Field(default=...)
    debug: bool = False
    secret_key: str = secrets.token_urlsafe(32)
    access_token_expire_minutes: int = 24 * 60 * 7  # 7 days
    activation_token_expire_seconds: int = 24 * 60 * 60  # 24 hours
    api_v1_str: str = "/api/v1"
    smtp_host: Optional[str] = None
    smtp_user: Optional[str] = None
    smtp_port: Optional[str] = None
    smtp_tls: bool = True
    smtp_password: Optional[str] = None
    sender_email_address: Optional[EmailStr] = None
    sender_email_name: Optional[str] = None
    emails_enabled: bool = False

    @validator("emails_enabled", pre=True)
    def get_emails_enabled(cls, _: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("smtp_host")
            and values.get("smtp_port")
            and values.get("sender_email_name")
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
