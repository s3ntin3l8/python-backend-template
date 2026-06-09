from fastapi import FastAPI

from app.core.logging import setup_logging

app = FastAPI(title="FastAPI Template")
logger = setup_logging(__name__)


@app.get("/")
async def root() -> dict[str, str]:
    logger.info("Hello World request")
    return {"message": "Hello World"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}
