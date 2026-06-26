"""
PGVector database operations.
"""

from psycopg.types.json import Json

from retrieval.config.settings import Settings
from retrieval.vectordb.connection import DatabaseConnection


class PGVectorStore:
    """
    Handles all PGVector database operations.
    """

    @staticmethod
    def create_table() -> None:
        """
        Create the legal_chunks table if it does not exist.
        """

        query = """
        CREATE TABLE IF NOT EXISTS legal_chunks (
            id SERIAL PRIMARY KEY,
            chunk_id TEXT UNIQUE,
            page_content TEXT NOT NULL,
            metadata JSONB,
            embedding VECTOR(384)
        );
        """

        conn = DatabaseConnection.connect()
        cur = conn.cursor()

        cur.execute(query)

        conn.commit()

        cur.close()
        conn.close()

    @staticmethod
    def insert_embeddings(documents: list) -> None:
        """
        Insert document embeddings into PGVector.
        """

        conn = DatabaseConnection.connect()
        cur = conn.cursor()

        query = """
        INSERT INTO legal_chunks
        (
            chunk_id,
            page_content,
            metadata,
            embedding
        )
        VALUES
        (%s, %s, %s, %s)
        ON CONFLICT (chunk_id)
        DO NOTHING;
        """

        for document in documents:

            cur.execute(
                query,
                (
                    document["chunk_id"],
                    document["page_content"],
                    Json(document["metadata"]),
                    document["embedding"],
                ),
            )

        conn.commit()

        cur.close()
        conn.close()

        print(f"✅ Inserted {len(documents)} embeddings.")

    @staticmethod
    def search(
        query_embedding: list[float],
        top_k: int = Settings.TOP_K,
    ) -> list:
        """
        Perform semantic similarity search.

        Args:
            query_embedding (list[float]): Query embedding vector.
            top_k (int): Number of results to return.

        Returns:
            list: Retrieved document chunks.
        """

        conn = DatabaseConnection.connect()
        cur = conn.cursor()

        query = """
        SELECT
            chunk_id,
            page_content,
            metadata,
            1 - (embedding <=> %s::vector) AS score
        FROM legal_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """

        cur.execute(
            query,
            (
                query_embedding,
                query_embedding,
                top_k,
            ),
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        results = []

        for row in rows:

            results.append(
                {
                    "chunk_id": row[0],
                    "page_content": row[1],
                    "metadata": row[2],
                    "score": float(row[3]),
                }
            )

        return results