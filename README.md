# Email Prioritizer with LLM Integration

This project is an **AI-powered email assistant** that automatically classifies emails, summarizes them, and suggests polite replies. It integrates with Gmail and uses large language models (LLMs) for natural language understanding. The processed emails are stored in a database for easy reference and analysis.

---

## Features

- **Email Classification:** Automatically categorize emails as `Urgent`, `Important`, or `FYI`.
- **Email Summarization:** Generate concise 1-2 sentence summaries of email content.
- **Reply Suggestions:** Suggest short, polite replies for emails.
- **Scheduler:** Automatically fetch new emails at configurable intervals.
- **Database Storage:** Store processed emails with priority, summary, and suggested reply.
- **Gmail Integration:** Fetch unread emails from your Gmail account.

---

## Tech Stack

- **Python 3.12**
- **FastAPI** – Web framework to run the application.
- **APScheduler** – Background scheduler for automatic email fetching.
- **SQLAlchemy** – ORM for database interaction (SQLite/PostgreSQL/MySQL).
- **Ollama / LLMs** – Large language models for classification, summarization, and reply generation.
- **Gmail API** – Fetch unread emails and create drafts.
- **html2text** – Convert email HTML content into plain text.
- **dotenv** – Load environment variables for configuration.

---

## Installation

1. **Clone the repository**
   
git clone https://github.com/Lovepreet1307/email-prioritizer.git
cd email-prioritizer

2. **Create a virtual environment and activate**

python -m venv venv
source venv/bin/activate

3. **Install dependencies**

pip install -r requirements.txt

4. **Set up environment variables (.env)**

GMAIL_CLIENT_ID=your_client_id_here

GMAIL_CLIENT_SECRET=your_client_secret_here

FETCH_INTERVAL_SECONDS=60

5. **Run the application**
   
uvicorn app.main:app --reload

## Gmail OAuth Setup

This project uses Gmail API to read and send emails. You need to set up OAuth credentials:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Enable the **Gmail API** for your project.
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth Client ID**.
5. Choose **Desktop App** and give it a name.
6. Download the JSON file containing your client secrets.
7. Save it as `credentials.json` in the project root directory.
8. On first run, the app will prompt you to authorize access via a URL. Follow the link and allow access.
9. The app will generate a `token.json` file to store the access token for future use.

