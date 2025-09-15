from fastapi import FastAPI, HTTPException
from .db import init_db, SessionLocal, EmailItem
from .worker import start_scheduler, process_new_emails
from pydantic import BaseModel
from typing import List
import threading

app = FastAPI(title="Email Prioritizer Agent")
init_db()

# start background scheduler in a separate thread
threading.Thread(target=start_scheduler, daemon=True).start()

class EmailOut(BaseModel):
    id: int
    sender: str
    subject: str
    priority: str
    summary: str
    suggested_reply: str

    class Config:
        orm_mode = True

@app.get("/emails/", response_model=List[EmailOut])
def list_emails(limit: int = 50):
    db = SessionLocal()
    items = db.query(EmailItem).order_by(EmailItem.processed_at.desc()).limit(limit).all()
    db.close()
    return items

@app.get("/emails/{email_id}", response_model=EmailOut)
def get_email(email_id: int):
    db = SessionLocal()
    item = db.query(EmailItem).get(email_id)
    db.close()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item

@app.post("/fetch-now/")
def fetch_now():
    try:
        process_new_emails()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
