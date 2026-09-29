"""
routers/contact.py — Contact form API endpoints.
Saves visitor messages to SQLite database and sends an email notification to Sumit.
"""
import smtplib
import logging
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import ContactMessage
from schemas import ContactFormIn, ContactMessageOut
from config import settings

router = APIRouter(prefix="/api/contact", tags=["Contact"])
logger = logging.getLogger("portfolio.contact")
logging.basicConfig(level=logging.INFO)


def send_email_notification(name: str, email: str, message: str, subject: Optional[str] = None) -> bool:
    """
    Send an email notification to Sumit's Gmail when a new message is received.
    Uses Reply-To header so replying directly in Gmail replies to the visitor.
    """
    sender = settings.GMAIL_SENDER or "sumitkhabra5911@gmail.com"
    receiver = settings.GMAIL_RECEIVER or "sumitkhabra5911@gmail.com"
    app_pwd = (settings.GMAIL_APP_PASSWORD or "").strip()

    if not app_pwd or app_pwd == "your-16-char-app-password-here":
        logger.warning(
            "⚠️ Gmail App Password not configured in backend/.env. "
            "Contact message saved safely in database, but email dispatch skipped. "
            "To enable live emails, generate a 16-character App Password at: "
            "https://myaccount.google.com/apppasswords and set GMAIL_APP_PASSWORD in backend/.env"
        )
        return False

    try:
        msg = MIMEMultipart("alternative")
        email_subj = f"📬 Portfolio Inquiry: {subject}" if subject else f"📬 New Portfolio Message from {name}"
        msg["Subject"] = email_subj
        msg["From"] = f"Portfolio Contact <{sender}>"
        msg["To"] = receiver
        msg["Reply-To"] = email

        # Formatted current timestamp
        current_time_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        # 1. Plain text version
        plain_text = (
            f"New Contact Message from Portfolio Website\n"
            f"-----------------------------------------\n"
            f"Sender Name : {name}\n"
            f"Sender Email: {email}\n"
            f"Topic/Subject: {subject or 'General Inquiry'}\n"
            f"Received    : {current_time_str}\n\n"
            f"Message Body:\n"
            f"{message}\n\n"
            f"-----------------------------------------\n"
            f"Reply directly to this email to contact {name}."
        )

        # 2. Rich HTML version
        topic_html = (
            f'<tr><td style="padding: 8px 0; color: #94a3b8; font-size: 14px;"><strong>Topic:</strong></td>'
            f'<td style="padding: 8px 0; color: #a78bfa; font-size: 15px; font-weight: 600;">{subject}</td></tr>'
        ) if subject else ""

        html_body = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin: 0; padding: 24px; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #f1f5f9;">
  <table width="100%" border="0" cellspacing="0" cellpadding="0">
    <tr>
      <td align="center">
        <table width="600" border="0" cellspacing="0" cellpadding="0" style="max-width: 600px; background: #121829; border: 1px solid rgba(0, 242, 254, 0.25); border-radius: 14px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.6);">
          <!-- Header -->
          <tr>
            <td style="padding: 28px 32px; background: linear-gradient(135deg, #1b233d 0%, #0d1222 100%); border-bottom: 1px solid rgba(255,255,255,0.08);">
              <div style="font-size: 13px; font-weight: 700; color: #00f2fe; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">
                Sumit Chauhan • Portfolio Contact Inquiry
              </div>
              <h1 style="margin: 0; font-size: 22px; font-weight: 700; color: #ffffff;">
                📬 New Message from {name}
              </h1>
            </td>
          </tr>
          <!-- Body Content -->
          <tr>
            <td style="padding: 28px 32px;">
              <table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin-bottom: 24px;">
                <tr>
                  <td style="padding: 8px 0; color: #94a3b8; font-size: 14px; width: 110px;"><strong>Sender Name:</strong></td>
                  <td style="padding: 8px 0; color: #f8fafc; font-size: 15px; font-weight: 600;">{name}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; color: #94a3b8; font-size: 14px;"><strong>Email:</strong></td>
                  <td style="padding: 8px 0; font-size: 15px;">
                    <a href="mailto:{email}" style="color: #00f2fe; text-decoration: none; font-weight: 600;">{email}</a>
                  </td>
                </tr>
                {topic_html}
                <tr>
                  <td style="padding: 8px 0; color: #94a3b8; font-size: 14px;"><strong>Received:</strong></td>
                  <td style="padding: 8px 0; color: #cbd5e1; font-size: 14px;">{current_time_str}</td>
                </tr>
              </table>

              <div style="font-size: 13px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                Message:
              </div>
              <div style="background: #0b0f19; border-left: 3px solid #00f2fe; border-radius: 8px; padding: 18px; color: #e2e8f0; font-size: 15px; line-height: 1.6; white-space: pre-wrap;">
{message}
              </div>

              <div style="margin-top: 28px; text-align: center;">
                <a href="mailto:{email}?subject=Re: Portfolio Inquiry" style="display: inline-block; background: linear-gradient(135deg, #00f2fe, #4facfe); color: #0b0f19; font-weight: 700; font-size: 14px; text-decoration: none; padding: 12px 28px; border-radius: 50px;">
                  ✉️ Reply Directly to {name}
                </a>
              </div>
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="padding: 18px 32px; background: rgba(0,0,0,0.25); border-top: 1px solid rgba(255,255,255,0.06); font-size: 12px; color: #64748b; text-align: center;">
              This notification was generated by your portfolio backend. Manage messages in your <a href="http://localhost:8000/admin" style="color: #00f2fe;">Admin Panel</a>.
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        # Dispatch via SMTP (SSL 465 first, fallback to TLS 587)
        email_sent = False
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=12) as server:
                server.login(sender, app_pwd)
                server.sendmail(sender, receiver, msg.as_string())
                email_sent = True
        except Exception as ssl_err:
            logger.warning(f"SMTP_SSL (port 465) failed: {ssl_err}. Attempting STARTTLS on port 587...")
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=12) as server:
                server.starttls()
                server.login(sender, app_pwd)
                server.sendmail(sender, receiver, msg.as_string())
                email_sent = True

        if email_sent:
            logger.info(f"✅ Notification email successfully sent to {receiver} for message from {email}")
            return True

    except Exception as e:
        logger.error(f"❌ Failed to dispatch email notification: {e}")
        return False


@router.get("/status")
async def contact_status():
    """Returns backend status and email routing configuration."""
    has_app_pwd = bool(
        settings.GMAIL_APP_PASSWORD and
        settings.GMAIL_APP_PASSWORD.strip() not in ("", "your-16-char-app-password-here")
    )
    return {
        "status": "online",
        "service": "Sumit Portfolio Contact API",
        "receiver_email": settings.GMAIL_RECEIVER,
        "email_delivery_configured": has_app_pwd
    }


@router.post("", response_model=ContactMessageOut, status_code=201)
@router.post("/", response_model=ContactMessageOut, status_code=201)
async def submit_contact_form(
    payload: ContactFormIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Accepts name, email, message, and optional subject.
    Validates input, records message to SQLite database, and queues an email notification.
    """
    clean_name = payload.name.strip()
    clean_email = payload.email.strip().lower()
    clean_message = payload.message.strip()
    clean_subject = payload.subject.strip() if payload.subject else None

    # Persist to database
    db_msg = ContactMessage(
        name=clean_name,
        email=clean_email,
        subject=clean_subject,
        message=clean_message
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)

    # Check if real email dispatch credentials are configured
    email_configured = bool(
        settings.GMAIL_APP_PASSWORD and
        settings.GMAIL_APP_PASSWORD.strip() not in ("", "your-16-char-app-password-here")
    )

    # Queue background task to send email notification
    background_tasks.add_task(
        send_email_notification,
        name=clean_name,
        email=clean_email,
        message=clean_message,
        subject=clean_subject
    )

    return ContactMessageOut(
        id=db_msg.id,
        name=db_msg.name,
        email=db_msg.email,
        subject=db_msg.subject,
        message=db_msg.message,
        submitted_at=db_msg.submitted_at or datetime.now(),
        is_read=db_msg.is_read,
        status="success",
        email_dispatched=email_configured
    )


@router.get("/messages", response_model=List[ContactMessageOut])
async def get_all_messages(db: Session = Depends(get_db)):
    """Return all contact messages (ordered newest first, used by admin panel)."""
    return db.query(ContactMessage).order_by(ContactMessage.submitted_at.desc()).all()


@router.patch("/{message_id}/read")
async def mark_as_read(message_id: int, db: Session = Depends(get_db)):
    """Mark a contact message as read."""
    msg = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    msg.is_read = True
    db.commit()
    return {"status": "ok"}


@router.delete("/{message_id}")
async def delete_message(message_id: int, db: Session = Depends(get_db)):
    """Delete a contact message."""
    msg = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()
    return {"status": "deleted"}
