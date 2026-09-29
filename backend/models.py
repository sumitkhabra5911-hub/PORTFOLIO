"""
models.py — SQLAlchemy ORM table definitions.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from database import Base


class ContactMessage(Base):
    """Stores messages submitted through the contact form."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    subject = Column(String(150), nullable=True)
    message = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)



class VisitorLog(Base):
    """Tracks every visit to the portfolio website."""
    __tablename__ = "visitor_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    browser = Column(String(100), nullable=True)
    os = Column(String(100), nullable=True)
    device = Column(String(50), nullable=True)
    page = Column(String(200), default="/")
    referrer = Column(String(500), nullable=True)
    visited_at = Column(DateTime, default=datetime.utcnow)
