"""
routers/portfolio.py — Portfolio data CRUD API endpoints.
Data is read from and written to portfolio_data.json.
"""
import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from schemas import BioUpdate

router = APIRouter(prefix="/api/portfolio", tags=["Portfolio"])

DATA_FILE = Path(__file__).parent.parent / "portfolio_data.json"


def _load() -> dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Read endpoints ────────────────────────────────────────────────────────────

@router.get("/")
async def get_all_portfolio_data():
    """Return the entire portfolio dataset."""
    return _load()


@router.get("/bio")
async def get_bio():
    return _load()["bio"]


@router.get("/projects")
async def get_projects():
    return _load()["projects"]


@router.get("/skills")
async def get_skills():
    return _load()["skills"]


@router.get("/education")
async def get_education():
    return _load()["education"]


@router.get("/experience")
async def get_experience():
    return _load()["experience"]


# ── Update endpoints (used by Admin Panel) ────────────────────────────────────

@router.patch("/bio")
async def update_bio(updates: BioUpdate):
    """Update bio fields. Only provided fields are changed."""
    data = _load()
    patch = updates.model_dump(exclude_none=True)
    data["bio"].update(patch)
    _save(data)
    return data["bio"]


@router.put("/projects/{project_id}")
async def update_project(project_id: int, payload: dict[str, Any]):
    """Replace a project card by its ID."""
    data = _load()
    for i, p in enumerate(data["projects"]):
        if p["id"] == project_id:
            data["projects"][i] = {**p, **payload, "id": project_id}
            _save(data)
            return data["projects"][i]
    raise HTTPException(status_code=404, detail="Project not found")


@router.post("/projects")
async def add_project(payload: dict[str, Any]):
    """Add a new project card."""
    data = _load()
    new_id = max((p["id"] for p in data["projects"]), default=0) + 1
    new_project = {**payload, "id": new_id}
    data["projects"].append(new_project)
    _save(data)
    return new_project


@router.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    """Remove a project card by ID."""
    data = _load()
    before = len(data["projects"])
    data["projects"] = [p for p in data["projects"] if p["id"] != project_id]
    if len(data["projects"]) == before:
        raise HTTPException(status_code=404, detail="Project not found")
    _save(data)
    return {"status": "deleted"}


@router.put("/skills/{skill_id}")
async def update_skill(skill_id: int, payload: dict[str, Any]):
    """Update a skill category."""
    data = _load()
    for i, s in enumerate(data["skills"]):
        if s["id"] == skill_id:
            data["skills"][i] = {**s, **payload, "id": skill_id}
            _save(data)
            return data["skills"][i]
    raise HTTPException(status_code=404, detail="Skill not found")
