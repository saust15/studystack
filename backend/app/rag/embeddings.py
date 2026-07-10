"""Embeddings via LiteLLM using OpenAI."""
from litellm import embedding

from app.config import settings

BATCH_SIZE = 100


def embed_texts(texts: list[str]) -> list[list[float]]:
    results: list[list[float]] = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        resp = embedding(
            model=settings.embedding_model,
            input=batch,
            api_key=settings.openai_api_key,
        )
        results.extend(d["embedding"] for d in resp.data)
    return results


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
