from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session_factory
from config import settings

# tạo session factory 1 lần
SessionFactory = get_session_factory(settings.SQLALCHEMY_DATABASE_URI)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session
