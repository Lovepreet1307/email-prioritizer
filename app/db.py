from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EmailItem(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String, unique=True, index=True)
    sender = Column(String)
    subject = Column(String)
    snippet = Column(Text)
    body = Column(Text)
    priority = Column(String, default="FYI")
    summary = Column(Text)
    suggested_reply = Column(Text)
    processed_at = Column(DateTime, default=datetime.datetime.utcnow)
    notified = Column(Boolean, default=False)

def init_db():
    Base.metadata.create_all(bind=engine)
