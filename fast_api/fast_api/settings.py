"""Application settings - paste this over your existing settings.py."""
import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FAST_API_",
        env_file_encoding="utf-8",
    )

    host: str = "127.0.0.1"
    port: int = 8000
    workers_count: int = 1
    reload: bool = False

    log_level: LogLevel = LogLevel.INFO

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "fast_api"
    db_pass: str = "fast_api"
    db_base: str = "fast_api"
    db_echo: bool = False

    # JWT — added for weather app auth
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # OpenWeatherMap — get free key at https://openweathermap.org/api
    openweather_api_key: str = ""

    @property
    def db_url(self) -> URL:
        """Assemble database URL from components."""
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )


settings = Settings()