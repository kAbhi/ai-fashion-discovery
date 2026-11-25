"""Application settings loaded from environment variables.

All configuration is environment-driven so the same code runs locally,
in preview and in production (Render) without modification.
"""

from functools import lru_cache
from typing import Annotated, Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Literal["local", "test", "preview", "production"] = "local"
    log_level: str = "INFO"

    # Required: no default, so a misconfigured deployment fails fast.
    database_url: str

    # Comma-separated list of allowed browser origins.
    cors_origins: Annotated[list[str], NoDecode] = []
    # Optional regex for origins that cannot be listed exactly (e.g. Vercel Preview URLs).
    # Intended for preview backends only; leave unset in production.
    cors_origin_regex: str | None = None

    # LLM configuration (used from Phase 2 onwards; never sent to the browser).
    llm_provider: str | None = None
    llm_api_key: str | None = None

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("database_url")
    @classmethod
    def _normalise_database_url(cls, value: str) -> str:
        """Force the psycopg (v3) driver.

        Render and most providers hand out ``postgres://`` or ``postgresql://``
        URLs; SQLAlchemy needs an explicit driver name to use psycopg 3.
        """
        for prefix in ("postgres://", "postgresql://"):
            if value.startswith(prefix):
                return "postgresql+psycopg://" + value[len(prefix) :]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()  # values come from the environment
