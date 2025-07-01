from fastapi import FastAPI
from app.api import health, version

app = FastAPI(title="Silph Users")

# Include base routes
app.include_router(health.router)
app.include_router(version.router)