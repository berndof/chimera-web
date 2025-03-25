from fastapi import FastAPI

from .models import Item
from .repository import ItemRepository
from .routes import router
from .service import ItemService


def register(app: FastAPI):
    app.include_router(router, prefix="/items", tags=["items"])
