"""
Pinecone vector database operations.
"""

from time import sleep

from pinecone import Pinecone, ServerlessSpec

from retrieval.config.settings import Settings


class PineconeStore:
    """
    Handles all Pinecone vector database operations.
    """

    def __init__(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
        from backend.app.core.diagnostic_logger import Profiler
        
        with Profiler("Pinecone client initialization"):
            self.pc = Pinecone(api_key=Settings.PINECONE_API_KEY)
            self.index_name = Settings.PINECONE_INDEX_NAME
            
        with Profiler("Pinecone create_index check"):
            self._create_index()

        with Profiler("Pinecone self.pc.Index"):
            self.index = self.pc.Index(
                self.index_name
            )

    def _create_index(self):
        """
        Create Pinecone index if it does not already exist.
        """

        existing_indexes = [
            index["name"]
            for index in self.pc.list_indexes()
        ]

        if self.index_name in existing_indexes:
            return

        print(f"Creating Pinecone Index: {self.index_name}")

        self.pc.create_index(
            name=self.index_name,
            dimension=Settings.EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            ),
        )

        while True:

            status = self.pc.describe_index(
                self.index_name
            )

            if status.status["ready"]:
                break

            print("Waiting for Pinecone index to become ready...")

            sleep(2)

        print("Pinecone index is ready.")

    def upsert(self, vectors):
        """
        Upload vectors to Pinecone.
        """

        self.index.upsert(
            vectors=vectors
        )

        print(f"Inserted {len(vectors)} vectors into Pinecone.")

    def search(
        self,
        query_embedding,
        top_k=Settings.TOP_K,
    ):
        """
        Perform semantic similarity search.
        """
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
        from backend.app.core.diagnostic_logger import Profiler

        with Profiler("Pinecone query"):
            response = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
            )

        results = []

        for match in response.matches:

            metadata = match.metadata or {}

            results.append(
                {
                    "chunk_id": match.id,
                    "page_content": metadata.get(
                        "page_content",
                        metadata.get("text", "")
                    ),
                    "metadata": metadata,
                    "score": float(match.score),
                }
            )

        return results