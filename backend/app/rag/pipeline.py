"""Core RAG pipeline shared by the CLI scripts and FastAPI service."""
import json
from dataclasses import dataclass

import psycopg
from litellm import completion

from app.config import settings
from app.rag.embeddings import embed_query

# pgvector: <=> is cosine DISTANCE (0 = identical). ORDER BY it, ascending.
RETRIEVE_SQL = """
SELECT b.title, c.chapter, c.content, (c.embedding <=> %s::vector) AS distance
FROM chunks c
JOIN books b ON b.id = c.book_id
ORDER BY c.embedding <=> %s::vector
LIMIT %s
"""

SYSTEM_PROMPT = """You are a study assistant. Answer ONLY from the provided context.
Cite sources inline like (Book Title, Chapter). If the context does not contain
the answer, say you don't know - do not invent information."""


@dataclass
class RetrievedChunk:
    book: str
    chapter: str
    content: str
    distance: float


def retrieve(question: str, k: int = 5) -> list[RetrievedChunk]:
    vec = json.dumps(embed_query(question))  # '[0.1, ...]' is a valid vector literal
    with psycopg.connect(settings.database_url) as conn:
        rows = conn.execute(RETRIEVE_SQL, (vec, vec, k)).fetchall()
    return [RetrievedChunk(*r) for r in rows]


def answer(question: str, chunks: list[RetrievedChunk]) -> str:
    context = "\n\n".join(f"[{c.book} - {c.chapter}]\n{c.content}" for c in chunks)
    resp = completion(
        model=settings.chat_model,
        api_key=(settings.anthropic_api_key if settings.chat_model.startswith("anthropic/") else settings.openai_api_key),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return resp.choices[0].message.content
