"""
config.py — Load environment variables from .env file.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "sumit")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "sumit@admin123")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    GMAIL_SENDER: str = os.getenv("GMAIL_SENDER", "sumitkhabra5911@gmail.com")
    GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")
    GMAIL_RECEIVER: str = os.getenv("GMAIL_RECEIVER", "sumitkhabra5911@gmail.com")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))

settings = Settings()

