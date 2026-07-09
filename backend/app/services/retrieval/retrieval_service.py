from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from urllib.parse import parse_qs, unquote, urlparse

from app.schemas.chunk import RetrievalResult

import sys
import os

# Add project root to path for Team B modules
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../../.."
        )
    )
)

from retrieval.search.retriever import Retriever
from retrieval.config.settings import Settings

DEFAULT_POSTGRES_PORT = 5432


def apply_database_url_settings(db_url: str, settings) -> None:
    parsed_url = urlparse(db_url)
    query_params = parse_qs(parsed_url.query)

    settings.DB_USER = unquote(parsed_url.username or "")
    settings.DB_PASSWORD = unquote(parsed_url.password or "")
    settings.DB_HOST = parsed_url.hostname or "localhost"
    settings.DB_PORT = parsed_url.port or DEFAULT_POSTGRES_PORT
    settings.DB_NAME = unquote(parsed_url.path.lstrip("/")) or "legal_rag"

    settings.DB_SSLMODE = query_params.get(
        "sslmode",
        query_params.get("ssl", [None])
    )[0]

    settings.DB_SSLROOTCERT = query_params.get(
        "sslrootcert",
        [None]
    )[0]

    settings.DB_SSLCERT = query_params.get(
        "sslcert",
        [None]
    )[0]

    settings.DB_SSLKEY = query_params.get(
        "sslkey",
        [None]
    )[0]

    settings.DB_APPLICATION_NAME = query_params.get(
        "application_name",
        [None]
    )[0]

    settings.DB_CONNECT_TIMEOUT = query_params.get(
        "connect_timeout",
        [None]
    )[0]


class RetrievalService:
    """
    Team B Retrieval Service.
    Handles semantic retrieval using Pinecone
    followed by CrossEncoder reranking.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

        # Sync Team B settings with backend database
        from app.core.settings import get_settings

        app_settings = get_settings()

        db_url = app_settings.DATABASE_URL

        if db_url:
            import urllib.parse

            parse_url = db_url.replace(
                "postgresql+asyncpg://",
                "postgresql://"
            )

            parsed = urllib.parse.urlparse(parse_url)

            Settings.DB_USER = parsed.username
            Settings.DB_PASSWORD = parsed.password
            Settings.DB_HOST = parsed.hostname
            Settings.DB_PORT = parsed.port or DEFAULT_POSTGRES_PORT
            Settings.DB_NAME = parsed.path.lstrip("/")

        self.retriever = Retriever()

    async def full_retrieve(
        self,
        query: str,
        top_k: int = Settings.TOP_K,
    ) -> List[RetrievalResult]:
        """
        Retrieve and rerank relevant document chunks.
        """

        import asyncio

        loop = asyncio.get_event_loop()

        results = await loop.run_in_executor(
            None,
            self.retriever.retrieve,
            query,
            top_k,
        )

        return [
            RetrievalResult(**result)
            for result in results
        ]