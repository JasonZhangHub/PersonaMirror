import json
import os
from datetime import datetime
from enum import Enum
from functools import lru_cache
from pathlib import Path

import requests
from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings


class PostgreSQLSettings(BaseModel):
    host: str = "localhost"
    database: str = "personamirror"
    username: str = "postgres"
    password: str = ""
    port: int = 5432
    ssl_mode: str = "prefer"
    db_schema: str = "public"

    @computed_field
    @property
    def url(self) -> str:
        """Construct PostgreSQL database URL."""
        return (
            f"postgresql://{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )


class DatabaseSettings(BaseModel):
    type: str = "sqlite"
    url: str = "sqlite:///./personamirror.db"


class OpenRouterSettings(BaseModel):
    api_key: str = ""
    base_url: str = "https://openrouter.ai/api/v1"
    model_name: str = "openai/gpt-4o"
    embedding_model_name: str = "openai/text-embedding-3-small"


class LoggingSettings(BaseModel):
    logs_dir: Path = Path.cwd() / "logs"
    log_format: str = (
        "%(asctime)s | " "%(name)s | " "%(levelname)s | " "%(pathname)s:%(funcName)s:%(lineno)d | " "%(message)s"
    )
    log_level: str = "DEBUG"
    run_timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")


class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

    database: DatabaseSettings = DatabaseSettings()
    postgresql: PostgreSQLSettings = PostgreSQLSettings()
    openrouter: OpenRouterSettings
    log: LoggingSettings = LoggingSettings()

    @computed_field
    @property
    def database_url(self) -> str:
        """Get the database URL based on the database type."""
        if self.database.type == "postgresql":
            return self.postgresql.url
        return self.database.url


@lru_cache()
def get_settings() -> Settings:
    """Get singleton settings instance."""
    return Settings()


# Singleton instance
app_settings = get_settings()
