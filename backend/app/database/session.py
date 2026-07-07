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

url_str = settings.DATABASE_URL
query_str = ""
try:
    import urllib.parse
    query_str = urllib.parse.urlparse(url_str).query
except:
    pass

connect_args = {
    "prepared_statement_cache_size": 0,
    "statement_cache_size": 0,
}

builtins.print("--- session.py create_async_engine config ---", flush=True)
builtins.print(f"DATABASE_URL (masked): {mask_url(url_str)}", flush=True)
builtins.print(f"DATABASE_URL query: {query_str}", flush=True)
builtins.print(f"connect_args: {connect_args}", flush=True)
builtins.print("---------------------------------------------", flush=True)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    poolclass=NullPool,
    connect_args=connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
