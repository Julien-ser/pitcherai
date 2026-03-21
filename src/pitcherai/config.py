"""Configuration management using Pydantic Settings."""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/pitcherai",
        description="Database connection URL",
    )

    # Redis (for Celery)
    redis_url: str = Field(
        default="redis://localhost:6379/0", description="Redis connection URL"
    )

    # API
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_debug: bool = Field(default=False, description="Debug mode")

    # Security
    secret_key: str = Field(
        default="change-me-in-production", description="JWT secret key"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")

    # OpenAI
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o-mini", description="OpenAI model to use")

    # Anthropic (optional)
    anthropic_api_key: str | None = Field(default=None, description="Anthropic API key")

    # Gmail API
    gmail_client_id: str | None = Field(
        default=None, description="Gmail OAuth client ID"
    )
    gmail_client_secret: str | None = Field(
        default=None, description="Gmail OAuth client secret"
    )
    gmail_refresh_token: str | None = Field(
        default=None, description="Gmail refresh token"
    )

    # Email sending
    default_from_email: str | None = Field(
        default=None, description="Default from email"
    )
    max_emails_per_day: int = Field(default=50, description="Rate limit for emails")
    email_frequency: int = Field(default=1, description="Seconds between emails")

    # Celery
    celery_broker_url: str = Field(
        default="redis://localhost:6379/1", description="Celery broker URL"
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/2", description="Celery result backend"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
