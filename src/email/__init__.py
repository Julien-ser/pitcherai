"""Gmail API integration."""


class GmailClient:
    """Client for Gmail API."""

    def __init__(self):
        self.authenticated = False

    async def authenticate(self):
        """Authenticate with Gmail API."""
        raise NotImplementedError("Gmail authentication not implemented yet")

    async def send_email(self, to, subject, body):
        """Send an email."""
        raise NotImplementedError("Email sending not implemented yet")

    async def check_responses(self):
        """Check for email responses."""
        raise NotImplementedError("Response checking not implemented yet")
