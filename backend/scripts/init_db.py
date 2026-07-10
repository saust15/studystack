"""Apply schema.sql to the database. Run once after `docker compose up -d`.
Usage (from backend/):  python scripts/init_db.py
"""
from pathlib import Path

import psycopg

from app.config import settings

SCHEMA = Path(__file__).parent.parent / "app" / "db" / "schema.sql"


def main() -> None:
    sql = SCHEMA.read_text()
    with psycopg.connect(settings.database_url) as conn:
        conn.execute(sql)
        conn.commit()
    print("Schema applied. Verify in pgAdmin: tables 'books' and 'chunks' should exist.")


if __name__ == "__main__":
    main()
