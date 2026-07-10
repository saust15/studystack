"""POST /ask - the RAG endpoint
"""
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.pipeline import answer, retrieve

router = APIRouter()


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    k: int = Field(default=5, ge=1, le=20)


class Citation(BaseModel):
    book: str
    chapter: str
    distance: float


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    latency_ms: int


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    start = time.perf_counter()
    chunks = retrieve(req.question, req.k)
    if not chunks:
        raise HTTPException(status_code=404, detail="No documents ingested yet.")
    text = answer(req.question, chunks)
    return AskResponse(
        answer=text,
        citations=[Citation(book=c.book, chapter=c.chapter, distance=round(c.distance, 4))
                   for c in chunks],
        latency_ms=int((time.perf_counter() - start) * 1000),
    )
