"""Configuration management using Pydantic Settings."""


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/pitcherai"
    redis_url: str = "redis://localhost:6379/0"

    # Gmail API
    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    gmail_refresh_token: str = ""

    # LLM API
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    default_model: str = "anthropic/claude-3.5-sonnet"

    # External APIs
    crunchbase_api_key: str | None = None
    angellist_access_token: str | None = None
    linkedin_client_id: str | None = None
    linkedin_client_secret: str | None = None

    # App Settings
    secret_key: str = "change-this-in-production"
    debug: bool = True
    app_env: str = "development"

    # Email Sending
    max_emails_per_day: int = 100
    email_rate_limit: int = 10  # per minute
    followup_days: int = 7

    # Dashboard
    dashboard_host: str = "0.0.0.0"
    dashboard_port: int = 8501
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
