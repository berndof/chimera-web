import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import start
from app.api import v1_api_router

logger = logging.getLogger("MAIN")
logger.setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # run something before the app starts
    logger.debug("Starting app...")
    await start.create_superuser_role()
    await start.create_superuser_user()
    # automatizar rotina de inicialização
    # verificar se as migrações do db estão em dia

    yield

    logger.debug("Shutting down...")


app = FastAPI(
    lifespan=lifespan,
    title=os.getenv("APP-TITLE", "Backend"),
    docs_url=os.getenv("API-DOCS-URL", "/api/docs"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_api_router, prefix="/api")
