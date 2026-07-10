-- Enables the vector data type + distance operators. Ships with the pgvector image.
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS books (
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    author      TEXT,
    topic       TEXT,              -- e.g. 'git', 'javascript', 'operating-systems'
    license     TEXT NOT NULL DEFAULT 'open',  -- 'open' or 'personal' (two-corpus design)
    source_file TEXT NOT NULL UNIQUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS chunks (
    id          SERIAL PRIMARY KEY,
    book_id     INT NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    chapter     TEXT,              -- chapter title breadcrumb, used in citations
    chunk_index INT NOT NULL,      -- position within the book
    content     TEXT NOT NULL,
    -- THE interesting column: a 1536-dim vector matching text-embedding-3-small.
    embedding   vector(1536) NOT NULL,
    UNIQUE (book_id, chunk_index)
);

-- HNSW index for fast approximate nearest-neighbor search.
-- vector_cosine_ops = index optimized for cosine distance (the <=> operator).
-- In Phase 3 you will benchmark this against IVFFlat.
CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw
    ON chunks USING hnsw (embedding vector_cosine_ops);
