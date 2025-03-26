# from app.config import module_list
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib import import_module
from os import getenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("LIFESPAN")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.debug("Starting app...")

    yield

    logger.debug("Shutting down...")


logger = logging.getLogger("MAIN")
logger.setLevel(logging.DEBUG)

modules_list = ["app.core"]


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title="API",
    )

    for module_path in modules_list:
        module = import_module(module_path)
        module.register(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()
