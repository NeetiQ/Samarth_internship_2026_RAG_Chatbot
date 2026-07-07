from uuid import uuid4

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from app.core.settings import get_settings

settings = get_settings()

import builtins
def mask_url(url_str: str) -> str:
    if not url_str: return ""
    try:
        import urllib.parse
        parsed = urllib.parse.urlparse(url_str)
        if parsed.password:
            return url_str.replace(parsed.password, "******")
    except: pass
    return url_str

builtins.print(f"session.py: Creating async engine with DATABASE_URL = {mask_url(settings.DATABASE_URL)}", flush=True)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    poolclass=NullPool,
    connect_args={
        "prepared_statement_cache_size": 0,
        "statement_cache_size": 0,
    },
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
