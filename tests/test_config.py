"""Tests for configuration module."""

from src.config import Settings


def test_settings_defaults():
    """Test default settings values."""
    settings = Settings()
    assert settings.debug is True
    assert (
        settings.database_url
        == "postgresql://postgres:password@localhost:5432/pitcherai"
    )
    assert settings.max_emails_per_day == 100


def test_settings_from_env(monkeypatch):
    """Test loading settings from environment."""
    monkeypatch.setenv("DEBUG", "False")
    monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/testdb")
    settings = Settings()
    assert settings.debug is False
    assert settings.database_url == "postgresql://test:test@localhost/testdb"
