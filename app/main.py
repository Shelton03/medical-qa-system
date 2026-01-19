from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import routes
from app.core.config import settings
from app.db.mongodb import db_client
from app.core.logger import logger
from app.services.nlp_service import initialize_qa_pipeline

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Medical QA System...")
    db_client.connect()
    initialize_qa_pipeline()
    yield
    # Shutdown
    logger.info("Shutting down Medical QA System...")
    db_client.close()

app = FastAPI(
    title="Medical QA System",
    description="Interactive Medical Question Answering System with Self-Consistency and Abstention",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(routes.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
