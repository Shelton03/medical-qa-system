from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import routes
from app.core.config import settings
from app.db.mongodb import db_client
from app.db.postgres import init_db, close_db
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Medical QA System...")
    db_client.connect()
    await init_db()
    yield
    logger.info("Shutting down Medical QA System...")
    db_client.close()
    await close_db()

app = FastAPI(
    title="Medical QA System",
    description="Interactive Medical Question Answering System with Self-Consistency and Abstention",
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
