"""POST /ingest - upload an epub."""
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, Header, HTTPException, UploadFile

from app.config import settings
from scripts.ingest import ingest_epub

router = APIRouter()


@router.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: str | None = Form(None),
    topic: str | None = Form(None),
    x_api_key: str = Header(default=""),
) -> dict:
    if x_api_key != settings.ingest_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if not (file.filename or "").endswith(".epub"):
        raise HTTPException(status_code=400, detail="Only .epub files supported")
    with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        return ingest_epub(tmp_path, title, author, topic)
    finally:
        Path(tmp_path).unlink(missing_ok=True)
