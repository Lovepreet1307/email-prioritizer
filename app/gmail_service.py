import base64
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from .config import GMAIL_OAUTH_CREDENTIALS_PATH, GMAIL_TOKEN_PATH
from typing import List, Dict
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.compose']

def build_gmail_service():
    creds = None
    if os.path.exists(GMAIL_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GMAIL_OAUTH_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # save token
        with open(GMAIL_TOKEN_PATH, 'w') as f:
            f.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_unread_messages(service, user_id='me', max_results=20):
    try:
        res = service.users().messages().list(userId=user_id, q="is:unread", maxResults=max_results).execute()
        msgs = res.get('messages', [])
        return msgs
    except HttpError as error:
        print("Gmail API error:", error)
        return []

def get_message(service, msg_id, user_id='me'):
    msg = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    payload = msg.get('payload', {})
    headers = payload.get('headers', [])
    parts = payload.get('parts', [])
    snippet = msg.get('snippet')
    sender = None
    subject = None
    for h in headers:
        if h['name'].lower() == 'from':
            sender = h['value']
        if h['name'].lower() == 'subject':
            subject = h['value']
    body = ''
    # extract body
    if 'parts' in payload and payload['parts']:
        for part in payload['parts']:
            mime = part.get('mimeType')
            if mime == 'text/plain' and part.get('body', {}).get('data'):
                body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
            elif mime == 'text/html' and part.get('body', {}).get('data'):
                body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
            elif part.get('parts'):
                # nested parts
                for sub in part.get('parts'):
                    if sub.get('body', {}).get('data'):
                        body += base64.urlsafe_b64decode(sub['body']['data']).decode('utf-8', errors='ignore')
    else:
        # sometimes body is in payload['body']
        if payload.get('body', {}).get('data'):
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')

    return {
        "id": msg.get('id'),
        "threadId": msg.get('threadId'),
        "sender": sender,
        "subject": subject,
        "snippet": snippet,
        "body": body
    }

def create_draft(service, to, subject, body_text, user_id='me'):
    message = {
        'raw': base64.urlsafe_b64encode(f"To: {to}\r\nSubject: {subject}\r\n\r\n{body_text}".encode()).decode()
    }
    draft = service.users().drafts().create(userId=user_id, body={'message': message}).execute()
    return draft
