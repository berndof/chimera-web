from fastapi import FastAPI

# TODO automatizar importação de submodulos
from .auth import router as auth_router
from .role import router as role_router
from .user import router as user_router


def register(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(role_router)
