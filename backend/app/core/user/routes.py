import logging

from fastapi import APIRouter, Depends

from app.core.role.dependencies import require_role
from app.core.user.dependencies import user_service
from app.core.user.schemas import UserCreate, UserResponse
from app.core.user.service import UserService

logger = logging.getLogger("USER_ROUTES")

all: list[str] = ["router"]
router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    current_role: str = Depends(require_role(["superuser"])),
    service: UserService = Depends(user_service),
):
    if current_role == "superuser":
        return await service.create(user_in)
