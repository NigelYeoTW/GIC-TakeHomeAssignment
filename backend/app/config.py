from pydantic_settings import BaseSettings
from functools import lru_cache
from enum import Enum


class Environment(str, Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    ENV: Environment = Environment.LOCAL
    APP_NAME: str = "Cafe Employee Manager"
    DEBUG: bool = False

    # Database
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # File upload
    UPLOAD_DIR: str = "uploads"
    MAX_LOGO_SIZE_BYTES: int = 2 * 1024 * 1024

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def is_production(self) -> bool:
        return self.ENV == Environment.PRODUCTION

    class Config:
        env_file_encoding = "utf-8"


class LocalSettings(Settings):
    DEBUG: bool = True
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        env_file = ".env.local"


class StagingSettings(Settings):
    DEBUG: bool = True

    class Config:
        env_file = ".env.staging"


class ProductionSettings(Settings):
    DEBUG: bool = False

    class Config:
        env_file = ".env.production"

@lru_cache()
def get_settings() -> Settings:
    import os
    env_str = os.getenv("ENV", Environment.LOCAL.value)
    try:
        env = Environment(env_str)
    except ValueError:
        env = Environment.LOCAL
    settings_map = {
        Environment.LOCAL: LocalSettings,
        Environment.STAGING: StagingSettings,
        Environment.PRODUCTION: ProductionSettings,
    }
    return settings_map.get(env, LocalSettings)()
