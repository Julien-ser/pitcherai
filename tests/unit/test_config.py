"""Tests for configuration module."""

import pytest
from pitcherai.config import Settings


def test_default_settings():
    """Test that default settings are loaded correctly."""
    settings = Settings()
    assert (
        settings.database_url
        == "postgresql+asyncpg://postgres:postgres@localhost:5432/pitcherai"
    )
    assert settings.redis_url == "redis://localhost:6379/0"
    assert settings.api_port == 8000
    assert settings.openai_model == "gpt-4o-mini"
    assert settings.max_emails_per_day == 50
    assert settings.celery_broker_url == "redis://localhost:6379/1"


def test_env_override(monkeypatch):
    """Test that environment variables override defaults."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost:5432/testdb")
    monkeypatch.setenv("API_PORT", "9000")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4")
    monkeypatch.setenv("MAX_EMAILS_PER_DAY", "100")

    settings = Settings()
    assert settings.database_url == "postgresql://test:test@localhost:5432/testdb"
    assert settings.api_port == 9000
    assert settings.openai_model == "gpt-4"
    assert settings.max_emails_per_day == 100
