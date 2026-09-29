"""
routers/analytics.py — Visitor tracking and analytics endpoints.
"""
from datetime import datetime, date, timedelta
from collections import Counter

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import VisitorLog
from schemas import VisitIn, VisitOut, AnalyticsStats

try:
    from user_agents import parse as ua_parse
    UA_AVAILABLE = True
except ImportError:
    UA_AVAILABLE = False

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


def _parse_ua(ua_string: str):
    """Parse user-agent string into browser/os/device info."""
    if not UA_AVAILABLE or not ua_string:
        return "Unknown", "Unknown", "Desktop"
    ua = ua_parse(ua_string)
    browser = ua.browser.family or "Unknown"
    os_name = ua.os.family or "Unknown"
    device = "Mobile" if ua.is_mobile else ("Tablet" if ua.is_tablet else "Desktop")
    return browser, os_name, device


@router.post("/visit", response_model=VisitOut, status_code=201)
async def log_visit(payload: VisitIn, request: Request, db: Session = Depends(get_db)):
    """Log a visitor. Called automatically by the frontend on page load."""
    ua_string = request.headers.get("user-agent", "")
    browser, os_name, device = _parse_ua(ua_string)

    # Get IP address (works behind proxies too)
    ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown")
    if "," in ip:
        ip = ip.split(",")[0].strip()

    log = VisitorLog(
        ip_address=ip,
        user_agent=ua_string[:500],
        browser=browser,
        os=os_name,
        device=device,
        page=payload.page or "/",
        referrer=payload.referrer
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/stats", response_model=AnalyticsStats)
async def get_analytics_stats(db: Session = Depends(get_db)):
    """Return aggregated visitor statistics for the admin dashboard."""
    all_visits = db.query(VisitorLog).all()
    total_visits = len(all_visits)

    today = date.today()
    today_visits = sum(1 for v in all_visits if v.visited_at and v.visited_at.date() == today)
    unique_ips = len(set(v.ip_address for v in all_visits if v.ip_address))

    # Top browsers
    browsers = Counter(v.browser for v in all_visits if v.browser)
    top_browsers = dict(browsers.most_common(5))

    # Top pages
    pages = Counter(v.page for v in all_visits if v.page)
    top_pages = dict(pages.most_common(5))

    # Visits by day (last 14 days)
    visits_by_day = {}
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        count = sum(1 for v in all_visits if v.visited_at and v.visited_at.date() == d)
        visits_by_day[str(d)] = count

    return AnalyticsStats(
        total_visits=total_visits,
        today_visits=today_visits,
        unique_ips=unique_ips,
        top_browsers=top_browsers,
        top_pages=top_pages,
        visits_by_day=visits_by_day
    )


@router.get("/recent", response_model=list[VisitOut])
async def get_recent_visits(limit: int = 50, db: Session = Depends(get_db)):
    """Return the most recent visitor log entries."""
    return (
        db.query(VisitorLog)
        .order_by(VisitorLog.visited_at.desc())
        .limit(limit)
        .all()
    )
