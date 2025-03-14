from fastapi import APIRouter

from app.core.routes import router as core
from app.user.routes import router as user

all = ["v1_api_router"]

v1_api_router = APIRouter(prefix="/v1")
v1_api_router.include_router(user)
v1_api_router.include_router(core)





