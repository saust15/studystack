"""Ingest one epub into Postgres.
"""
import argparse
import json

import psycopg

from app.config import settings
from app.rag.chunking import build_chunk, chunk_text
from app.rag.embeddings import embed_texts
from app.rag.epub_loader import load_epub


def ingest_epub(epub_path: str, title: str, author: str | None,
                topic: str | None, license_: str = "open") -> dict:
    chapters = load_epub(epub_path)
    print(f"Loaded {len(chapters)} chapters from {title!r}")

    rows: list[tuple[str, str]] = []  # (chapter_title, chunk_content)
    for ch in chapters:
        for piece in chunk_text(ch.text):
            rows.append((ch.title, build_chunk(title, ch.title, piece)))
    print(f"Built {len(rows)} chunks; embedding (batched)...")

    vectors = embed_texts([content for _, content in rows])
    assert len(vectors) == len(rows)

    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO books (title, author, topic, license, source_file)
                   VALUES (%s, %s, %s, %s, %s)
                   ON CONFLICT (source_file) DO UPDATE SET title = EXCLUDED.title
                   RETURNING id""",
                (title, author, topic, license_, epub_path),
            )
            book_id = cur.fetchone()[0]
            cur.execute("DELETE FROM chunks WHERE book_id = %s", (book_id,))  # re-ingest safety
            cur.executemany(
                """INSERT INTO chunks (book_id, chapter, chunk_index, content, embedding)
                   VALUES (%s, %s, %s, %s, %s)""",
                [
                    (book_id, chap, i, content, json.dumps(vec))
                    for i, ((chap, content), vec) in enumerate(zip(rows, vectors))
                ],
            )
        conn.commit()
    print(f"Ingested book_id={book_id} with {len(rows)} chunks.")
    return {"book_id": book_id, "chapters": len(chapters), "chunks": len(rows)}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("epub_path")
    p.add_argument("--title", required=True)
    p.add_argument("--author", default=None)
    p.add_argument("--topic", default=None)
    p.add_argument("--license", default="open", choices=["open", "personal"])
    args = p.parse_args()
    ingest_epub(args.epub_path, args.title, args.author, args.topic, args.license)


if __name__ == "__main__":
    main()
