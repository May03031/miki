from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.auth import router as auth_router
from config import settings
from app.models.domain import Base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.engine import get_engine, wait_for_db
from app.db.base import Base
from config import settings

from sqlalchemy.ext.asyncio import AsyncEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
     # Startup: Print config or warm up connections
    print(f"Starting {settings.PROJECT_NAME}")
    
    engine: AsyncEngine = get_engine()

    # ⏳ Đợi DB (KHÔNG crash)
    await wait_for_db(engine)

    # Optional: create tables (DEV only)
    if settings.AUTO_CREATE_TABLES:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    yield


##@asynccontextmanager
##async def lifespan(app: FastAPI):
##    # Startup: Print config or warm up connections
##    print(f"Starting {settings.PROJECT_NAME}")
    
##    # In Dev: Auto-create tables (Use Alembic in Prod!)
##    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
##    async with engine.begin() as conn:
##         await conn.run_sync(Base.metadata.create_all)
    
##    yield
##    # Shutdown logic here
    

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])

@app.get("/health")
def health_check():
    return {"status": "ok"}