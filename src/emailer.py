# emailer module for ai-daily-brief

import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_gmail_service():
    """Create a Gmail API service using OAuth credentials from the environment.
    Requires the following environment variables to be set:
    GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN.
    """
    creds = Credentials(
        token=None,
        refresh_token=os.getenv("GMAIL_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GMAIL_CLIENT_ID"),
        client_secret=os.getenv("GMAIL_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/gmail.send"],
    )
    return build("gmail", "v1", credentials=creds)

def send_email(to: str, subject: str, body: str):
    """Send a simple email via the Gmail API.
    Args:
        to: Recipient email address.
        subject: Email subject.
        body: Plain‑text email body.
    """
    service = get_gmail_service()
    message_text = f"To: {to}\nSubject: {subject}\n\n{body}"
    raw_message = base64.urlsafe_b64encode(message_text.encode("utf-8")).decode("utf-8")
    message = {"raw": raw_message}
    try:
        result = service.users().messages().send(userId="me", body=message).execute()
        print(f"Message sent, id: {result.get('id')}")
    except Exception as e:
        print(f"Failed to send email: {e}")
