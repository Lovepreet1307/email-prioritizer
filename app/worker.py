import time
from apscheduler.schedulers.background import BackgroundScheduler
from .gmail_service import build_gmail_service, list_unread_messages, get_message
from .db import SessionLocal, EmailItem
from .llm_service import classify_email, summarize_email, suggest_reply
from .utils import html_to_text
from .config import FETCH_INTERVAL_SECONDS
from sqlalchemy.exc import IntegrityError
import threading

# Global lock to prevent overlapping job executions
job_lock = threading.Lock()

def process_new_emails_safe():
    """Wrapper that ensures only one job runs at a time."""
    if not job_lock.acquire(blocking=False):
        print("Job already running, skipping this interval")
        return

    try:
        process_new_emails()
    except Exception as e:
        print("Error in job:", e)
    finally:
        job_lock.release()

def process_new_emails():
    """Fetch and process new emails."""
    service = build_gmail_service()
    msgs = list_unread_messages(service)
    if not msgs:
        return

    db = SessionLocal()
    for m in msgs:
        detail = get_message(service, m['id'])
        body = detail.get('body') or detail.get('snippet') or ""
        body_text = html_to_text(body)

        # LLM analysis
        classification = classify_email(body_text)
        summary = summarize_email(body_text)
        reply = suggest_reply(body_text)

        item = EmailItem(
            gmail_id=detail['id'],
            sender=detail.get('sender'),
            subject=detail.get('subject'),
            snippet=detail.get('snippet'),
            body=body_text,
            priority=classification['priority'],
            summary=summary,
            suggested_reply=reply
        )
        try:
            db.add(item)
            db.commit()
            db.refresh(item)
        except IntegrityError:
            db.rollback()
            continue

    db.close()

def start_scheduler():
    """Start the scheduler with safe job execution."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        process_new_emails_safe,
        'interval',
        seconds=FETCH_INTERVAL_SECONDS,
        max_instances=1  # APScheduler also prevents overlaps
    )
    scheduler.start()
    print("Scheduler started. Fetch interval:", FETCH_INTERVAL_SECONDS)

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler shutdown")
