"""RUNIX application configuration.

Loads settings from environment variables with validated defaults.
Secrets are never logged or exposed in API responses.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """RUNIX backend configuration derived from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "RUNIX"
    app_version: str = "0.1.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    api_port: int = 8000
    log_level: str = "INFO"

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./runix_dev.db"
    )
    database_echo: bool = False

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")

    # Security
    jwt_secret: str = Field(default="super_secret_jwt_key_change_in_production")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    session_secret: str = Field(default="super_secret_session_key")

    # CORS
    cors_origins: list[str] = Field(default=["http://localhost:3000"])

    # Runtime
    runtime_container_network: str = "runix-sandbox-net"
    workspace_base_dir: str = "/tmp/runix/workspaces"  # noqa: S108

    # GitHub OAuth
    github_client_id: str = ""
    github_client_secret: str = ""
    github_callback_url: str = "http://localhost:8000/api/v1/auth/github/callback"

    # AI
    ai_api_key: str = ""
    ai_model_name: str = "gemini-1.5-pro"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
