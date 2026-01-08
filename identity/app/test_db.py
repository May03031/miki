import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

engine = create_async_engine(
    "postgresql+asyncpg://ai_user:123456@db:5432/kimi_system"
)

async def test():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print("✅ SQLAlchemy CONNECT OK:", result.scalar())

asyncio.run(test())
