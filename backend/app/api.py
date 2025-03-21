from fastapi import APIRouter

from app.core.auth import router as auth_router
from app.core.health import router as health_router
from app.core.role import router as role_router
from app.core.user import router as user_router

all = ["v1_api_router"]

v1_api_router = APIRouter(prefix="/v1")

v1_api_router.include_router(user_router)
v1_api_router.include_router(role_router)

v1_api_router.include_router(auth_router)
v1_api_router.include_router(health_router)
