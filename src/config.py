"""Configuration management for PitcheRai."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Application settings from environment variables."""

    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./pitcherai.db")

    # APIs
    openrouter_api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    crunchbase_api_key: Optional[str] = os.getenv("CRUNCHBASE_API_KEY")
    angellist_access_token: Optional[str] = os.getenv("ANGELLIST_ACCESS_TOKEN")

    # Gmail
    gmail_client_id: Optional[str] = os.getenv("GMAIL_CLIENT_ID")
    gmail_client_secret: Optional[str] = os.getenv("GMAIL_CLIENT_SECRET")
    gmail_refresh_token: Optional[str] = os.getenv("GMAIL_REFRESH_TOKEN")

    # Email settings
    email_rate_limit: int = int(os.getenv("EMAIL_RATE_LIMIT", "100"))  # per day
    email_from_address: Optional[str] = os.getenv("EMAIL_FROM_ADDRESS")
    email_from_name: Optional[str] = os.getenv("EMAIL_FROM_NAME", "Founder")

    # LLM settings
    default_model: str = os.getenv("DEFAULT_MODEL", "openai/gpt-4o")

    # Redis/Celery
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # App settings
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
