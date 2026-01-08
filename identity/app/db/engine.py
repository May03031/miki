import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import text
from config import settings
import logging

logger = logging.getLogger(__name__)

_engine: AsyncEngine | None = None


#def get_engine(database_url: str) -> AsyncEngine:
#    global _engine
#    if _engine is None:
#        _engine = create_async_engine(
#           database_url,
#           pool_pre_ping=True,
#            echo=False,
#       )
#    return _engine

def get_engine() -> AsyncEngine:
    global _engine

    if _engine is None:
        _engine = create_async_engine(
            settings.SQLALCHEMY_DATABASE_URI,
            pool_pre_ping=True,
            echo=False,
        )

    return _engine


async def wait_for_db(
    engine: AsyncEngine,
    retries: int = 10,
    delay: float = 2.0,
):
    """
    Retry DB connection, KHÔNG làm app chết
    """
    for attempt in range(1, retries + 1):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("✅ Database ready")
            return
        except Exception as e:
            logger.warning(
                f"⏳ DB not ready (attempt {attempt}/{retries}): {e}"
            )
            await asyncio.sleep(delay)

    logger.error("❌ Database not ready after retries")
