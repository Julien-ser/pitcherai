"""Configuration management using Pydantic Settings."""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI
    openai_api_key: str = Field("", env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4-turbo-preview", env="OPENAI_MODEL")
    openai_max_tokens: int = Field(500, env="OPENAI_MAX_TOKENS")
    openai_temperature: float = Field(0.7, env="OPENAI_TEMPERATURE")

    # Gmail API
    gmail_client_id: str = Field("", env="GMAIL_CLIENT_ID")
    gmail_client_secret: str = Field("", env="GMAIL_CLIENT_SECRET")
    gmail_refresh_token: str = Field("", env="GMAIL_REFRESH_TOKEN")
    gmail_access_token: str = Field("", env="GMAIL_ACCESS_TOKEN")

    # Database
    database_url: str = Field("sqlite:///pitcherai.db", env="DATABASE_URL")

    # Application
    app_env: str = Field("development", env="APP_ENV")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    debug: bool = Field(True, env="DEBUG")

    # Collector
    crunchbase_api_key: str = Field("", env="CRUNCHBASE_API_KEY")
    angellist_api_key: str = Field("", env="ANGELLIST_API_KEY")
    news_api_key: str = Field("", env="NEWS_API_KEY")

    # Campaign
    default_campaign_delay_days: int = Field(7, env="DEFAULT_CAMPAIGN_DELAY_DAYS")
    max_emails_per_day: int = Field(50, env="MAX_EMAILS_PER_DAY")
    user_email: str = Field("", env="USER_EMAIL")
    user_name: str = Field("", env="USER_NAME")
    user_company: str = Field("", env="USER_COMPANY")
    user_description: str = Field("", env="USER_DESCRIPTION")

    # Email template
    default_draft_template: str = Field(
        "Hi {{name}},\n\nI noticed your recent investment in {{recent_investment}} and believe our startup aligns with your thesis.\n\nWe're building {{company_description}} and would love to share more.\n\nWould you be open to a 15-minute call?\n\nBest,\n{{sender_name}}",
        env="DEFAULT_DRAFT_TEMPLATE",
    )

    # Learning
    enable_learning: bool = Field(True, env="ENABLE_LEARNING")
    min_responses_for_learning: int = Field(10, env="MIN_RESPONSES_FOR_LEARNING")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
