from fastapi import APIRouter

from app.core.routes import auth_router, health_router
from app.core.user.routes import router as user_router

all = ["v1_api_router"]

v1_api_router = APIRouter(prefix="/v1")
v1_api_router.include_router(user_router)
v1_api_router.include_router(auth_router)
v1_api_router.include_router(health_router)
