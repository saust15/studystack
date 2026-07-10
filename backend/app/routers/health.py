"""Liveness + DB connectivity"""
import psycopg
from fastapi import APIRouter

from app.config import settings

router = APIRouter()


@router.get("/health")
def health() -> dict:
    try:
        with psycopg.connect(settings.database_url, connect_timeout=3) as conn:
            conn.execute("SELECT 1")
        db = "ok"
    except Exception:
        db = "unreachable"
    return {"status": "ok" if db == "ok" else "degraded", "db": db}
