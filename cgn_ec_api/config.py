from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    HOOKS_DIRECTORY: Path = Path(__file__).parent.joinpath("hooks")
    RAISE_ERROR_FROM_HOOK: bool = True

    CORS_ORIGINS: list[str] = [
        "http://localhost:8000",
    ]
    CORS_HEADERS: list[str] = ["*"]

    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DEFAULT_LOOKBACK_HOURS: int = 3

    API_KEY_HEADER: str = "x-api-key"
    API_KEYS: list[str] = ["default-change-me"]

    REDIS_URI: str = "redis://localhost:6379"
    REDIS_PASSWORD: str = "Pa55w0rd!"
    CACHE_EXPIRE: int = 7200


settings = Settings()
