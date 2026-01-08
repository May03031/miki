from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)
from .engine import get_engine


def get_session_factory(database_url: str):
    engine = get_engine()

    return async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
