import os
from dotenv import load_dotenv
load_dotenv()

GMAIL_OAUTH_CREDENTIALS_PATH = os.getenv("GMAIL_OAUTH_CREDENTIALS_PATH", "oauth_credentials.json")
GMAIL_TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "token.json")
#NOTIFY_WEBHOOK = os.getenv("NOTIFY_WEBHOOK")  # optional
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./email_agent.db")
FETCH_INTERVAL_SECONDS = int(os.getenv("FETCH_INTERVAL_SECONDS", "120"))  # poll every 60s
