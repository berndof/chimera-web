from fastapi import APIRouter, Depends

from app.core.user.dependencies import user_service
from app.core.user.schemas import UserCreate, UserResponse
from app.core.user.service import UserService

all = ["router"]
router = APIRouter(prefix="/user", tags=["user"])


@router.post("/users/create", response_model=UserResponse)
async def create_user(
    user_in: UserCreate, service: UserService = Depends(user_service)
):
    return await service.create(user_in)
