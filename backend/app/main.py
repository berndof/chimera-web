__all__ = ["app"]

import logging
from contextlib import asynccontextmanager
from importlib import import_module

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import submodules_path_list

logger = logging.getLogger("MAIN")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Starting lifespan")
    try:
        #await start.create_defaults()
        yield
        logger.debug("Ending lifespan")
    except Exception as e:
        logger.error(f"Error during lifespan: {e}")
        raise

def create_app() -> FastAPI:
    logger.debug("Creating FastAPI app")
    app = FastAPI(
        lifespan=lifespan,
        title="Backend API"
    )

    #import submodules
    for submodule_path in submodules_path_list if submodules_path_list else []:
        module = import_module(submodule_path)
        module.register(app)

    #TODO SET CORS FOR FQDN
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()
    