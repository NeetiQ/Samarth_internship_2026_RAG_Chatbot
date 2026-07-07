import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "../.env"), override=False)

from app.database.base import Base
import app.models.all_models  # To ensure models are loaded
from app.core.settings import get_settings

config = context.config
settings = get_settings()

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

import traceback

def run_migrations_offline() -> None:
    print("START Database Migration (Offline)", flush=True)
    try:
        url = settings.DATABASE_URL
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )
        with context.begin_transaction():
            context.run_migrations()
        print("END Database Migration (Offline)", flush=True)
    except Exception as e:
        print(f"DATABASE MIGRATION ERROR (Offline): {e}", flush=True)
        traceback.print_exc()
        raise

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
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

    builtins.print("--- env.py async_engine_from_config config ---", flush=True)
    builtins.print(f"alembic env.py: settings.DATABASE_URL = {mask_url(settings.DATABASE_URL)}", flush=True)
    builtins.print(f"alembic env.py: PGSSLMODE in os.environ = {os.environ.get('PGSSLMODE')}", flush=True)
    builtins.print(f"alembic env.py: PGSSLROOTCERT in os.environ = {os.environ.get('PGSSLROOTCERT')}", flush=True)
    builtins.print(f"DATABASE_URL query: {query_str}", flush=True)
    builtins.print("-----------------------------------------------", flush=True)

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=settings.DATABASE_URL
    )

    builtins.print("--- env.py before connectable.connect() ---", flush=True)
    builtins.print(f"connectable.url (masked): {mask_url(str(connectable.url))}", flush=True)
    builtins.print(f"connectable.url.query: {connectable.url.query if hasattr(connectable, 'url') else 'N/A'}", flush=True)
    builtins.print("-------------------------------------------", flush=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    print("START Database Migration (Online)", flush=True)
    try:
        asyncio.run(run_async_migrations())
        print("END Database Migration (Online)", flush=True)
    except Exception as e:
        print(f"DATABASE MIGRATION ERROR (Online): {e}", flush=True)
        traceback.print_exc()
        raise

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
