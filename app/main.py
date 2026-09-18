from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from app.api import routes
from app.core.config import settings
from app.db.postgres import close_db
from app.db.storage import StorageClient
from app.core.logger import logger
from alembic.config import Config
from alembic import command


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Mirage backend...")
    # Run Alembic migrations instead of SQLAlchemy create_all.
    # Alembic is synchronous, so offload it from the async event loop.
    alembic_cfg = Config("alembic.ini")
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")

    # Initialize object storage (synchronous boto3 calls).
    storage = StorageClient(settings)
    await asyncio.to_thread(storage.ensure_bucket)

    yield
    logger.info("Shutting down Mirage backend...")
    await close_db()


app = FastAPI(
    title="Mirage",
    description="Mirage healthcare platform API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/api")

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "mirage-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
