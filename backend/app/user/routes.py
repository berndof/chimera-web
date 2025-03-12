from fastapi import APIRouter, Depends

from app.user.dependencies import user_service
from app.user.schemas import UserCreate, UserResponse

all = ["router"]
router = APIRouter(prefix="/user", tags=["user"])

@router.post(
    "/users/create", response_model=UserResponse
)
async def create_user(user_in: UserCreate, service = Depends(user_service)) -> UserResponse:
    return await service.create(user_in)
