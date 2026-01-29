from fastapi import FastAPI
from app.routers.stream import router as stream_router
from app.database import engine, Base

app = FastAPI(title="AI Call Ingestion Service")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(stream_router)

@app.get("/health")
async def health():
    return {"status": "ok"}