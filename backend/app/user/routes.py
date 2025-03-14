from fastapi import APIRouter, Depends

from app.user.dependencies import user_service
from app.user.schemas import UserCreate, UserResponse
from app.user.service import UserService

all = ["router"]
router = APIRouter(prefix="/user", tags=["user"])

@router.post(
    "/users/create", response_model=UserResponse
)
async def create_user(
    user_in: UserCreate, service:UserService = Depends(user_service)
):
    return await service.create(user_in)
