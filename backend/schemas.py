"""
schemas.py — Pydantic v2 data validation schemas.
"""
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, EmailStr, Field, field_validator


# ── Contact Form ──────────────────────────────────────────────────────────────

class ContactFormIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of sender")
    email: EmailStr = Field(..., description="Valid email address of sender")
    message: str = Field(..., min_length=10, max_length=5000, description="Message content")
    subject: Optional[str] = Field(None, max_length=150, description="Inquiry topic or subject")

    @field_validator("name", "message", mode="before")
    @classmethod
    def strip_and_validate(cls, value: str) -> str:
        if isinstance(value, str):
            val = value.strip()
            if not val:
                raise ValueError("Field cannot be blank or only whitespace.")
            return val
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if len(value.strip()) < 2:
            raise ValueError("Name must be at least 2 characters.")
        return value.strip()


class ContactMessageOut(BaseModel):
    id: int
    name: str
    email: str
    subject: Optional[str] = None
    message: str
    submitted_at: datetime
    is_read: bool = False
    status: str = "success"
    email_dispatched: bool = False

    model_config = {"from_attributes": True}



# ── Visitor Analytics ─────────────────────────────────────────────────────────

class VisitIn(BaseModel):
    page: Optional[str] = "/"
    referrer: Optional[str] = None

class VisitOut(BaseModel):
    id: int
    ip_address: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    device: Optional[str] = None
    page: Optional[str] = None
    visited_at: datetime

    model_config = {"from_attributes": True}

class AnalyticsStats(BaseModel):
    total_visits: int
    today_visits: int
    unique_ips: int
    top_browsers: Dict[str, int]
    top_pages: Dict[str, int]
    visits_by_day: Dict[str, int]


# ── Admin Auth ────────────────────────────────────────────────────────────────

class AdminLogin(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Portfolio Data ────────────────────────────────────────────────────────────

class BioUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    title: Optional[str] = None
    tagline: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    current_role: Optional[str] = None
    open_to_roles: Optional[bool] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
