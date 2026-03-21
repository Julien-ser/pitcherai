"""Email module - Gmail API integration and email sending"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from typing import Dict, List, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ..config.config import settings
from ..database import get_db, Email, EmailStatus, Investor


class GmailSender:
    """Handles Gmail API operations"""

    def __init__(self):
        self.service = None
        self.initialized = False

    def _get_credentials(self) -> Optional[Credentials]:
        """Create credentials from settings"""
        if not all(
            [settings.gmail_client_id, settings.gmail_client_secret, settings.gmail_refresh_token]
        ):
            return None

        return Credentials(
            token=None,
            refresh_token=settings.gmail_refresh_token,
            token_uri=settings.gmail_token_uri,
            client_id=settings.gmail_client_id,
            client_secret=settings.gmail_client_secret,
        )

    def initialize(self) -> bool:
        """Initialize Gmail service"""
        try:
            creds = self._get_credentials()
            if not creds:
                print("Gmail credentials not configured")
                return False

            self.service = build("gmail", "v1", credentials=creds)
            self.initialized = True
            return True
        except Exception as e:
            print(f"Failed to initialize Gmail service: {e}")
            return False

    def create_message(
        self, to: str, subject: str, body: str, html_body: Optional[str] = None
    ) -> Dict:
        """Create email message dict"""
        if html_body:
            message = MIMEMultipart("alternative")
            text_part = MIMEText(body, "plain")
            html_part = MIMEText(html_body, "html")
            message.attach(text_part)
            message.attach(html_part)
        else:
            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        return {"raw": raw_message}

    def send_message(self, message: Dict) -> Optional[str]:
        """Send email via Gmail API"""
        if not self.initialized:
            if not self.initialize():
                return None

        try:
            sent_message = self.service.users().messages().send(userId="me", body=message).execute()
            return sent_message.get("id")
        except HttpError as e:
            print(f"Gmail API error: {e}")
            return None

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email and return success status"""
        message = self.create_message(to, subject, body)
        message_id = self.send_message(message)
        return message_id is not None


class EmailManager:
    """Manages email sending and tracking"""

    def __init__(self):
        self.gmail = GmailSender()

    def mark_as_sent(self, email_id: int, message_id: str) -> bool:
        """Mark an email as sent with Gmail message ID"""
        db = get_db()
        try:
            email = db.query(Email).filter_by(id=email_id).first()
            if email:
                email.status = EmailStatus.SENT
                email.message_id = message_id
                email.sent_at = datetime.utcnow()
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error marking email as sent: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def send_pending_email(self, email_id: int) -> bool:
        """Send a pending draft email"""
        db_gen = get_db()
        db = next(db_gen)
        try:
            email = db.query(Email).filter_by(id=email_id).first()
            if not email or email.status != "draft":
                return False

            if not email.investor or not email.investor.email:
                print(f"No recipient email for email {email_id}")
                return False

            success = self.gmail.send_email(
                to=email.investor.email, subject=email.subject, body=email.body
            )

            if success:
                self.mark_as_sent(email_id, email.message_id or "")
                # Also update investor status
                if email.investor:
                    email.investor.status = "contacted"
                    email.investor.last_contacted_at = datetime.utcnow()
                    db.commit()

            return success

        except Exception as e:
            print(f"Error sending email {email_id}: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def send_batch(self, email_ids: List[int]) -> Dict[int, bool]:
        """Send multiple emails"""
        results = {}
        for email_id in email_ids:
            results[email_id] = self.send_pending_email(email_id)
        return results


def create_email_sender() -> EmailManager:
    """Factory function for EmailManager"""
    return EmailManager()
