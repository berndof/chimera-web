import logging

from fastapi import APIRouter, Depends

from app.core.user.dependencies import get_current_user, user_service
from app.core.user.model import User
from app.core.user.schemas import UserCreate, UserResponse
from app.core.user.service import UserService

logger = logging.getLogger("USER_ROUTES")

all: list[str] = ["router"]
router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(user_service)
):
    #check permission level

    response = await service.create(user_in)
    return response
