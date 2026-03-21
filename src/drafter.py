"""Email drafting with LLM."""


class LLMClient:
    """Client for OpenRouter LLM API."""

    def __init__(self, api_key=None, model=None):
        self.api_key = api_key
        self.model = model

    async def generate(self, prompt):
        """Generate text from LLM."""
        raise NotImplementedError("LLM generation not implemented yet")


class Personalizer:
    """Personalize email drafts for investors."""

    def __init__(self):
        pass

    def draft_email(
        self, startup, investor, template_variant, founder_name, founder_email
    ):
        """Draft a personalized email."""
        raise NotImplementedError("Email drafting not implemented yet")
