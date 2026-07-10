# StudyStack

RAG study companion for a CS bookshelf — chat with your technical ebooks, get
answers grounded in real chapters with citations.

**Status: Phase 1** — EPUB ingestion → pgvector → retrieval → grounded answers (CLI).

## Stack
Python 3.11+ · PostgreSQL 16 + pgvector (Docker) · OpenAI embeddings + gpt-4o-mini · psycopg3

## Quickstart
```
docker compose up -d
cd backend && uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"
cp ../.env.example .env   # add your OpenAI key
python scripts/init_db.py
python scripts/ingest.py ../data/epubs/progit.epub --title "Pro Git" --topic git
python scripts/ask.py "How does git rebase differ from merge?"
```

