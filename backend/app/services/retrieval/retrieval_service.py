from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.schemas.chunk import RetrievalResult
from app.repositories import chunk_repo

import sys
import os

# Add root of the project to path for Team B's scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from retrieval.search.retriever import Retriever

class RetrievalService:
    def __init__(self, db: AsyncSession):
        self.db = db
        # Set Team B's settings to match backend DB settings
        from retrieval.config.settings import Settings
        from app.core.settings import get_settings
        app_settings = get_settings()
        
        # Override DB settings for Team B's raw psycopg connection
        # Expected URL format: postgresql+asyncpg://user:password@host:port/dbname
        db_url = app_settings.DATABASE_URL
        if db_url:
            db_url = db_url.replace("postgresql+asyncpg://", "")
            credentials, host_port_db = db_url.split("@")
            user, password = credentials.split(":")
            host_port, dbname = host_port_db.split("/")
            host, port = host_port.split(":")
            
            Settings.DB_USER = user
            Settings.DB_PASSWORD = password
            Settings.DB_HOST = host
            Settings.DB_PORT = int(port)
            Settings.DB_NAME = dbname
        else:
            Settings.DB_NAME = "legal_rag"
            
        Settings.TOP_K = 5
        
        self.retriever = Retriever()

    async def full_retrieve(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
        # Team B's retriever is synchronous, run in executor
        import asyncio
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, self.retriever.retrieve, query, top_k)
        
        # results are dicts matching RetrievalResult perfectly thanks to our schema update
        return [RetrievalResult(**r) for r in results]
