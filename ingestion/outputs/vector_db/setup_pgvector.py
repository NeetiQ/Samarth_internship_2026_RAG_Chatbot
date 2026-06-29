import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS legal_chunks (
            chunk_id TEXT PRIMARY KEY,
            page_content TEXT NOT NULL,
            metadata JSONB,
            embedding VECTOR(384)
        );
    """)

    conn.commit()

    cur.close()
    conn.close()

    print("PGVector table setup completed.")


if __name__ == "__main__":
    main()