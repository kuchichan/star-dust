from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    database_dsn: PostgresDsn = Field(default=...)
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
