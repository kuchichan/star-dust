from pydantic import BaseSettings
from pydantic.fields import Field
from pydantic.networks import PostgresDsn


class Settings(BaseSettings):
    database_dsn: PostgresDsn = Field(default=...)
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
