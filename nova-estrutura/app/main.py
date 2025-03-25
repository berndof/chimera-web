import logging
from importlib import import_module
from os import getenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import module_list
from app.core.lifespan import lifespan

logger = logging.getLogger("MAIN")
logger.setLevel(logging.DEBUG)


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title=getenv("APP_TITLE", "backend"),
        docs_url=getenv("API_DOCS", "/api/docs"),
    )

    for module_path in module_list:
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
