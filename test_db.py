import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        "postgresql://ai_user:123456@db:5432/kimi_system",
        ssl=False
    )
    print("✅ CONNECT OK")
    await conn.close()

asyncio.run(test())

