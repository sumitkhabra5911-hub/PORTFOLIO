"""
main.py — FastAPI application entry point.
Run with: uvicorn main:app --reload --port 8000
API docs: http://localhost:8000/docs
Admin panel: http://localhost:8000/admin
"""
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from schemas import AdminLogin, TokenOut
from config import settings

# Import routers
from routers import contact, analytics, portfolio

# ── App initialization ────────────────────────────────────────────────────────

app = FastAPI(
    title="Sumit Chauhan — Portfolio Backend",
    description="Backend API powering the portfolio website of Sumit Chauhan (Data Analyst & AI Specialist).",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ── CORS — allow frontend to call the API ─────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production, change to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Create DB tables on startup ───────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    print("\n[OK] Database tables created / verified.")
    print("[UP] Portfolio Backend started!")
    print("     API Docs:    http://localhost:8000/docs")
    print("     Admin Panel: http://localhost:8000/admin\n")

# ── Register routers ──────────────────────────────────────────────────────────
app.include_router(contact.router)
app.include_router(analytics.router)
app.include_router(portfolio.router)

# ── Simple in-memory token store ──────────────────────────────────────────────
_active_tokens: dict = {}


def _verify_token(token: str) -> bool:
    exp = _active_tokens.get(token)
    if not exp:
        return False
    if datetime.utcnow() > exp:
        _active_tokens.pop(token, None)
        return False
    return True


# ── Admin Auth Endpoints ──────────────────────────────────────────────────────

@app.post("/api/admin/login", response_model=TokenOut)
async def admin_login(payload: AdminLogin):
    if (payload.username != settings.ADMIN_USERNAME or
            payload.password != settings.ADMIN_PASSWORD):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = secrets.token_urlsafe(32)
    _active_tokens[token] = datetime.utcnow() + timedelta(hours=8)
    return TokenOut(access_token=token)


@app.get("/api/admin/verify")
async def verify_token(request: Request):
    token = request.headers.get("x-admin-token") or request.cookies.get("admin_token")
    if not token or not _verify_token(token):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"status": "ok"}


# ── Admin Panel (serve HTML) ──────────────────────────────────────────────────

ADMIN_HTML = Path(__file__).parent / "static" / "admin.html"

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel():
    if not ADMIN_HTML.exists():
        raise HTTPException(status_code=404, detail="Admin panel not found")
    return ADMIN_HTML.read_text(encoding="utf-8")


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat(),
        "service": "Sumit Chauhan Portfolio Backend"
    }


# ── Frontend Static Hosting ───────────────────────────────────────────────────
FRONTEND_DIR = Path(__file__).parent.parent
INDEX_HTML = FRONTEND_DIR / "index.html"

@app.get("/style.css")
async def get_css():
    css_file = FRONTEND_DIR / "style.css"
    if css_file.exists():
        return FileResponse(css_file, media_type="text/css")
    raise HTTPException(status_code=404, detail="style.css not found")

@app.get("/script.js")
async def get_js():
    js_file = FRONTEND_DIR / "script.js"
    if js_file.exists():
        return FileResponse(js_file, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="script.js not found")

@app.get("/profile.jpg")
async def get_profile():
    img_file = FRONTEND_DIR / "profile.jpg"
    if img_file.exists():
        return FileResponse(img_file, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="profile.jpg not found")

@app.get("/", response_class=HTMLResponse)
async def root():
    if INDEX_HTML.exists():
        return HTMLResponse(content=INDEX_HTML.read_text(encoding="utf-8"), status_code=200)
    return HTMLResponse(content="<h1>Portfolio Backend Running</h1><p>Visit <a href='/admin'>/admin</a> or <a href='/docs'>/docs</a>.</p>")

