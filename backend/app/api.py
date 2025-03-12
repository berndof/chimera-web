from fastapi import APIRouter

from app.user.routes import router

all = ["v1_api_router"]

v1_api_router = APIRouter(prefix="/v1")
v1_api_router.include_router(router)





