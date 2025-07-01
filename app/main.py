import asyncio
from app.db.session import engine
from app.models import user
from app.models.base import Base
from fastapi import FastAPI
from app.api import health, version

app = FastAPI(title="Silph Users")

# Include base routes
app.include_router(health.router)
app.include_router(version.router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    