"""Gmail API service for sending emails."""

import base64
from email.mime.text import MIMEText
from typing import Optional, List
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

from ..config import settings


class GmailService:
    """Service for sending emails via Gmail API."""

    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    def __init__(self):
        self.creds = self._get_credentials()
        self.service = None
        if self.creds:
            self.service = build("gmail", "v1", credentials=self.creds)

    def _get_credentials(self):
        """Get Gmail API credentials."""
        # Check for refresh token (simplified for demo)
        if not all(
            [
                settings.gmail_client_id,
                settings.gmail_client_secret,
                settings.gmail_refresh_token,
            ]
        ):
            return None

        creds = Credentials(
            token=None,
            refresh_token=settings.gmail_refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.gmail_client_id,
            client_secret=settings.gmail_client_secret,
            scopes=self.SCOPES,
        )

        # Refresh if needed
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        return creds

    def create_message(
        self, to_email: str, subject: str, body: str, from_email: Optional[str] = None
    ) -> dict:
        """Create an email message."""
        from_addr = from_email or settings.default_from_email
        if not from_addr:
            raise ValueError("No from email configured")

        message = MIMEText(body, "plain", "utf-8")
        message["to"] = to_email
        message["from"] = from_addr
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        return {"raw": raw_message}

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None,
    ) -> Optional[str]:
        """Send an email via Gmail API."""
        if not self.service:
            print("Gmail service not configured")
            return None

        try:
            message = self.create_message(to_email, subject, body, from_email)

            # Run in executor to avoid blocking
            import asyncio

            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: (
                    self.service.users()
                    .messages()
                    .send(userId="me", body=message)
                    .execute()
                ),
            )

            return result.get("id")

        except HttpError as e:
            print(f"Gmail API error: {e}")
            return None
        except Exception as e:
            print(f"Error sending email: {e}")
            return None

    async def send_bulk_emails(
        self,
        emails: List[dict],
        delay_seconds: int = 1,
    ) -> List[Optional[str]]:
        """Send multiple emails with rate limiting."""
        import asyncio

        results = []
        for email in emails:
            to_email = email["to_email"]
            subject = email["subject"]
            body = email["body"]
            from_email = email.get("from_email")

            message_id = await self.send_email(to_email, subject, body, from_email)
            results.append(message_id)

            # Rate limiting
            if delay_seconds > 0 and email != emails[-1]:
                await asyncio.sleep(delay_seconds)

        return results


# Global instance
gmail_service = GmailService()
