"""Tests for Email Generation service."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from openai import AsyncOpenAI

from pitcherai.services.email_generation import EmailGenerationService
from pitcherai.config import settings


class TestEmailGenerationService:
    """Tests for EmailGenerationService."""

    @pytest.fixture
    def email_service(self):
        """Create a fresh email service instance."""
        return EmailGenerationService()

    def test_init(self, email_service):
        """Test service initialization."""
        assert email_service.model == settings.openai_model
        assert email_service._client is None

    async def test_client_lazy_initialization(self, email_service):
        """Test that OpenAI client is lazily initialized."""
        assert email_service._client is None
        if settings.openai_api_key:
            client = email_service.client
            assert client is not None
            assert isinstance(client, AsyncOpenAI)

    def test_build_context_basic(self, email_service):
        """Test building context with basic data."""
        context = email_service._build_context(
            investor_name="John Doe",
            investor_firm="VC Firm",
            investor_focus=["AI", "ML"],
            investor_recent_investments=None,
            user_startup="MyStartup",
            user_description="A cool startup",
            user_niche="tech",
            custom_vars={},
        )

        assert context["investor_name"] == "John Doe"
        assert context["investor_firm"] == "VC Firm"
        assert context["investor_focus"] == "AI, ML"
        assert context["investor_recent_investments"] == ""
        assert context["user_startup"] == "MyStartup"
        assert context["user_niche"] == "tech"

    def test_build_context_with_recent_investments(self, email_service):
        """Test building context with recent investments."""
        investments = [
            {"startup_name": "Startup1", "round_type": "Seed"},
            {"startup_name": "Startup2", "round_type": "Series A"},
        ]

        context = email_service._build_context(
            investor_name="Jane Doe",
            investor_firm=None,
            investor_focus=["SaaS"],
            investor_recent_investments=investments,
            user_startup="MyStartup",
            user_description="My startup description",
            user_niche="SaaS",
            custom_vars={"custom_key": "custom_value"},
        )

        assert "Startup1" in context["investor_recent_investments"]
        assert "Startup2" in context["investor_recent_investments"]
        assert context["custom_key"] == "custom_value"

    def test_build_context_with_custom_vars(self, email_service):
        """Test that custom vars are merged into context."""
        custom = {"var1": "value1", "var2": "value2"}
        context = email_service._build_context(
            investor_name="Test",
            investor_firm="",
            investor_focus=[],
            investor_recent_investments=[],
            user_startup="Startup",
            user_description="Desc",
            user_niche="Niche",
            custom_vars=custom,
        )

        assert context["var1"] == "value1"
        assert context["var2"] == "value2"

    def test_fill_template_simple(self, email_service):
        """Test simple template filling."""
        template = "Hello {{investor_name}}, we're {{user_startup}}"
        context = {
            "investor_name": "John",
            "user_startup": "MyStartup",
        }

        result = email_service._fill_template(template, context)

        assert result == "Hello John, we're MyStartup"

    def test_fill_template_with_multiple_placeholders(self, email_service):
        """Test template filling with multiple placeholders."""
        template = "Dear {{investor_name}} from {{investor_firm}}, I'm {{user_startup}}"
        context = {
            "investor_name": "Jane",
            "investor_firm": "VC Firm",
            "user_startup": "MyStartup",
        }

        result = email_service._fill_template(template, context)
        assert result == "Dear Jane from VC Firm, I'm MyStartup"

    def test_fill_template_with_extra_context_keys(self, email_service):
        """Test that extra context keys are ignored."""
        template = "Hello {{investor_name}}"
        context = {
            "investor_name": "John",
            "extra_key": "should be ignored",
        }

        result = email_service._fill_template(template, context)
        assert result == "Hello John"
        assert "extra_key" not in result

    @pytest.mark.skipif(
        settings.openai_api_key is None, reason="OpenAI API key not configured"
    )
    async def test_generate_email_with_ai(self, email_service):
        """Test email generation with actual AI (requires API key)."""
        subject, body = await email_service.generate_email(
            investor_name="John Doe",
            investor_firm="VC Firm",
            investor_focus=["AI", "ML"],
            investor_recent_investments=[
                {"startup_name": "TechCo", "round_type": "Seed"}
            ],
            user_startup="MyAIStartup",
            user_description="An AI startup building cool stuff",
            user_niche="Artificial Intelligence",
            template_subject="Introduction: {{user_startup}}",
            template_body="Hello {{investor_name}}, I'm building {{user_startup}}...",
        )

        assert subject is not None
        assert len(subject) > 0
        assert body is not None
        assert len(body) > 0

    async def test_generate_email_without_api_key(self, email_service):
        """Test email generation when OpenAI client is not available."""
        # Temporarily disable client
        original_client = email_service._client
        email_service._client = None

        subject, body = await email_service.generate_email(
            investor_name="John Doe",
            investor_firm="VC Firm",
            investor_focus=["AI"],
            investor_recent_investments=[],
            user_startup="MyStartup",
            user_description="A startup",
            user_niche="tech",
            template_subject="Hello {{investor_name}}",
            template_body="Hi {{investor_name}}, we're {{user_startup}}",
        )

        # Without AI, should return template with filled placeholders
        assert subject == "Hello John Doe"
        assert "Hi John Doe" in body
        assert "MyStartup" in body

        # Restore client
        email_service._client = original_client

    async def test_generate_email_with_custom_vars(self, email_service):
        """Test email generation with custom variables."""
        # Mock the client
        email_service._client = AsyncMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Enhanced body"))]
        email_service._client.chat.completions.create.return_value = mock_response

        subject, body = await email_service.generate_email(
            investor_name="John",
            investor_firm="Firm",
            investor_focus=["AI"],
            investor_recent_investments=[],
            user_startup="Startup",
            user_description="Desc",
            user_niche="tech",
            template_subject="Hi {{investor_name}} - {{custom_var}}",
            template_body="Body with {{custom_var}}",
            custom_vars={"custom_var": "custom_value"},
        )

        assert "custom_value" in subject
        assert (
            "custom_value" in body
        )  # Should be in base template before AI enhancement

    async def test_enhance_with_ai_success(self, email_service):
        """Test successful AI enhancement."""
        # Mock the OpenAI client
        email_service._client = AsyncMock()
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Enhanced email body"))
        ]
        email_service._client.chat.completions.create.return_value = mock_response

        result = await email_service._enhance_with_ai(
            investor_name="John Doe",
            investor_firm="VC Firm",
            investor_focus=["AI"],
            investor_recent_investments=[],
            user_startup="MyStartup",
            user_description="A startup",
            user_niche="tech",
            base_body="Base email body",
            custom_vars={},
        )

        assert result == "Enhanced email body"

        # Verify the API was called with correct parameters
        email_service._client.chat.completions.create.assert_called_once()
        call_args = email_service._client.chat.completions.create.call_args
        assert call_args.kwargs["model"] == email_service.model
        assert len(call_args.kwargs["messages"]) == 2
        assert call_args.kwargs["messages"][0]["role"] == "system"

    async def test_enhance_with_ai_error_fallback(self, email_service):
        """Test that AI enhancement falls back to base body on error."""
        email_service._client = AsyncMock()
        email_service._client.chat.completions.create.side_effect = Exception(
            "API Error"
        )

        base_body = "Base email content"
        result = await email_service._enhance_with_ai(
            investor_name="John",
            investor_firm="Firm",
            investor_focus=[],
            investor_recent_investments=[],
            user_startup="Startup",
            user_description="Desc",
            user_niche="tech",
            base_body=base_body,
            custom_vars={},
        )

        # Should return base body unchanged on error
        assert result == base_body

    async def test_enhance_with_ai_no_client(self, email_service):
        """Test AI enhancement when client is None."""
        email_service._client = None
        base_body = "Base body"
        result = await email_service._enhance_with_ai(
            investor_name="John",
            investor_firm="",
            investor_focus=[],
            investor_recent_investments=[],
            user_startup="Startup",
            user_description="Desc",
            user_niche="tech",
            base_body=base_body,
            custom_vars={},
        )

        assert result == base_body
