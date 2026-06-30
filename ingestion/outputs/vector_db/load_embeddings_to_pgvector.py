import os
import json
import psycopg2
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
INPUT_FILE = "data/embedded_documents.jsonl"


def vector_to_sql(embedding):
    return "[" + ",".join(str(x) for x in embedding) + "]"


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    inserted = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            record = json.loads(line)

            page_content = record["page_content"]
            metadata = record["metadata"]
            embedding = record["embedding"]
            chunk_id = metadata.get("chunk_id")

            if not chunk_id:
                continue

            cur.execute(
                """
                INSERT INTO legal_chunks (
                chunk_id,
                page_content,
                metadata,
                embedding
            )
                )
                VALUES (%s, %s, %s, %s::vector)
                ON CONFLICT (chunk_id) DO UPDATE SET
                    page_content = EXCLUDED.page_content,
                    metadata = EXCLUDED.metadata,
                    embedding = EXCLUDED.embedding;
                """,
                (
                    chunk_id,
                    page_content,
                    json.dumps(metadata),
                    vector_to_sql(embedding),
                ),
            )

            inserted += 1

            if inserted % 500 == 0:
                conn.commit()
                print(f"Inserted {inserted} records...")

    conn.commit()

    cur.close()
    conn.close()

    print(f"Done. Total records loaded: {inserted}")


if __name__ == "__main__":
    main()