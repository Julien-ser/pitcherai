"""Gmail integration and email tracking."""

import base64
import logging
from email.mime.text import MIMEText
from typing import Any, List, Optional
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.models import Outreach
from src.config import settings

logger = logging.getLogger(__name__)


class GmailClient:
    """Gmail API client for sending and tracking emails."""

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
    ]

    def __init__(self, credentials: dict[str, str] = None):
        self.credentials = credentials or {}
        self.service = None

    async def authenticate(
        self, token_path: str = "token.json", credentials_path: str = "credentials.json"
    ):
        """Authenticate with Gmail API."""
        creds = None
        if token_path:
            try:
                creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
            except Exception as e:
                logger.warning(f"Failed to load token: {e}")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Failed to refresh credentials: {e}")
                    creds = None
            else:
                # Use provided credentials to create flow
                if self.credentials.get("client_id") and self.credentials.get(
                    "client_secret"
                ):
                    flow = InstalledAppFlow.from_client_config(
                        {
                            "installed": {
                                "client_id": self.credentials["client_id"],
                                "client_secret": self.credentials["client_secret"],
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token",
                            }
                        },
                        self.SCOPES,
                    )
                    creds = flow.run_local_server(port=0)
                else:
                    logger.error("No valid credentials provided")
                    return False

            # Save credentials
            if token_path and creds:
                with open(token_path, "w") as token:
                    token.write(creds.to_json())

        try:
            self.service = build("gmail", "v1", credentials=creds)
            logger.info("Gmail API authenticated successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
            return False

    async def send_email(
        self, to: str, subject: str, body: str, thread_id: str = None
    ) -> dict[str, Any]:
        """Send an email via Gmail API."""
        if not self.service:
            raise RuntimeError(
                "Gmail service not authenticated. Call authenticate() first."
            )

        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject

        # Add headers for threading and tracking
        if thread_id:
            message["In-Reply-To"] = thread_id
            message["References"] = thread_id

        try:
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            body = {"raw": raw_message}
            if thread_id:
                body["threadId"] = thread_id

            result = (
                self.service.users().messages().send(userId="me", body=body).execute()
            )
            logger.info(f"Email sent to {to}, message ID: {result.get('id')}")
            return {"id": result.get("id"), "threadId": result.get("threadId")}
        except HttpError as e:
            logger.error(f"Gmail API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise

    async def check_replies(
        self, message_id: str = None, days_back: int = 7
    ) -> List[dict[str, Any]]:
        """Check for replies to sent messages."""
        if not self.service:
            raise RuntimeError(
                "Gmail service not authenticated. Call authenticate() first."
            )

        try:
            # Search for messages that are replies to our sent messages
            query = f"label:sent newer_than:{days_back}d"
            if message_id:
                query += f" in:threadthread:{message_id}"

            results = (
                self.service.users().messages().list(userId="me", q=query).execute()
            )
            messages = results.get("messages", [])

            replies = []
            for msg in messages:
                msg_data = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=msg["id"], format="metadata")
                    .execute()
                )
                headers = msg_data.get("payload", {}).get("headers", [])
                subject = next(
                    (h["value"] for h in headers if h["name"] == "Subject"), ""
                )
                from_email = next(
                    (h["value"] for h in headers if h["name"] == "From"), ""
                )
                date = next((h["value"] for h in headers if h["name"] == "Date"), "")

                # Check if it's a reply (subject starts with Re: or contains previous subject)
                is_reply = subject.lower().startswith("re:") or "Re:" in subject

                if is_reply:
                    replies.append(
                        {
                            "id": msg["id"],
                            "subject": subject,
                            "from": from_email,
                            "date": date,
                            "snippet": msg_data.get("snippet", ""),
                        }
                    )

            return replies
        except Exception as e:
            logger.error(f"Failed to check replies: {e}")
            return []


class EmailSender:
    """Manage sending queue and rate limits."""

    def __init__(self, gmail_client: GmailClient, rate_limit: int = 10):
        self.gmail_client = gmail_client
        self.rate_limit = rate_limit  # emails per minute
        self.send_queue: List[Outreach] = []
        self.last_send_time = 0

    def queue_email(self, outreach: Outreach):
        """Add email to send queue."""
        self.send_queue.append(outreach)

    async def process_queue(self, db_session):
        """Process send queue with rate limiting."""
        sent_count = 0
        errors = []

        while self.send_queue:
            # Check rate limit
            current_time = time.time()
            time_since_last = current_time - self.last_send_time
            if time_since_last < (60 / self.rate_limit):
                wait_time = (60 / self.rate_limit) - time_since_last
                logger.debug(f"Rate limiting: waiting {wait_time:.2f} seconds")
                time.sleep(wait_time)

            outreach = self.send_queue.pop(0)
            try:
                result = await self.gmail_client.send_email(
                    to=outreach.investor_id,  # This should be investor email, not ID - need to fix
                    subject=outreach.subject,
                    body=outreach.body,
                )
                outreach.sent_at = time.time()  # Should be datetime
                outreach.status = "sent"
                self.last_send_time = time.time()
                sent_count += 1

                # Save to database
                # TODO: Update outreach in DB
                logger.info(f"Sent outreach {outreach.id} to {outreach.investor_id}")

            except Exception as e:
                logger.error(f"Failed to send outreach {outreach.id}: {e}")
                outreach.status = "bounced"
                errors.append(str(e))

        return {"sent": sent_count, "errors": errors, "remaining": len(self.send_queue)}

    async def send_batch(self, batch_size: int = 10, db_session=None):
        """Send a batch of emails."""
        batch = self.send_queue[:batch_size]
        for outreach in batch:
            self.send_queue.remove(outreach)
            # Mark as queued first
            outreach.status = "queued"
            # This is simplified; should persist to DB
        return await self.process_queue(db_session)


class ResponseTracker:
    """Track email responses and categorise them."""

    def __init__(self, gmail_client: GmailClient):
        self.gmail_client = gmail_client

    def categorize_response(self, email_body: str) -> str:
        """Categorize reply as interested/not_interested/maybe_later."""
        # Simple keyword matching (to be replaced with ML)
        text = email_body.lower()
        if any(
            word in text
            for word in [
                "interested",
                "let's talk",
                "schedule",
                "call",
                "meeting",
                "love to learn more",
            ]
        ):
            return "interested"
        elif any(
            word in text
            for word in ["not interested", "no thanks", "pass", "decline", "not a fit"]
        ):
            return "not_interested"
        else:
            return "maybe_later"

    async def update_outreach_status(self, outreach: Outreach, email_body: str):
        """Update outreach based on response."""
        response_type = self.categorize_response(email_body)
        outreach.response = email_body[:500]  # Truncate
        outreach.response_type = response_type
        outreach.status = "replied"
        return outreach

    async def track_all_responses(self, db_session):
        """Check for new responses and update all outreaches."""
        # Get all sent outreaches that don't have responses yet
        # TODO: Query from database
        # For now, just check replies
        replies = await self.gmail_client.check_replies()
        return replies
