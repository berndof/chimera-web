# from app.config import module_list
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib import import_module

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .start import start


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.debug("Starting app...")
    try:
        await start()
        yield
        logger.debug("Shutting down...")
    except Exception as e:
        logger.error(f"ad {e}")
        # sys.exit(0)


logger = logging.getLogger("MAIN")

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
