from fastapi import FastAPI

from .models import User
from .repository import UserRepository
from .routes import router
from .service import UserService


def register(app: FastAPI):
    app.include_router(router)
