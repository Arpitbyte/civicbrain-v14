"""Database engine, session management, and connectivity diagnostics."""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from civicbrain.infra.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base declarative class for all CivicBrain database entities."""

    pass


# Initialize async engine
connect_args: dict[str, int] = {}
if "postgresql" in settings.DATABASE_URL:
    connect_args["statement_cache_size"] = 0
    connect_args["prepared_statement_cache_size"] = 0

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    poolclass=NullPool,
    future=True,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides an async session per request."""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_connection() -> tuple[bool, str]:
    """Verifies that the database is reachable and PostGIS is enabled.

    Returns:
        (is_connected, message)
    """
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1;"))
            val = result.scalar()
            if val == 1:
                # Also check PostGIS availability if present
                try:
                    gis_res = await conn.execute(text("SELECT PostGIS_Version();"))
                    gis_ver = gis_res.scalar()
                    return True, f"Connected. PostGIS Version: {gis_ver}"
                except Exception:
                    return True, "Connected (PostGIS check skipped or extension not yet created)"
            return False, "Database returned unexpected response"
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        return False, str(e)
