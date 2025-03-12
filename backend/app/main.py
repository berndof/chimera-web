import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import v1_api_router
from app.core.database import populate_sqlite

logger = logging.getLogger("MAIN")
logger.setLevel(logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # run something before the app starts
    logger.debug("Starting app...")

    if os.getenv("ENV") == "dev":
        await populate_sqlite()

    yield

    logger.debug("Shutting down...")

app = FastAPI(
    lifespan = lifespan,
    title = os.getenv("APP-TITLE", "Backend"),
    docs_url = os.getenv("API-DOCS-URL", "/api/docs"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_api_router, prefix="/api")
