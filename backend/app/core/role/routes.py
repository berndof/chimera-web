import logging

from fastapi import APIRouter, Depends

from app.core.role.dependencies import role_service
from app.core.role.schemas import RoleCreate, RoleResponse
from app.core.role.service import RoleService

logger = logging.getLogger("ROLE_ROUTES")

all: list[str] = ["router"]
router = APIRouter(prefix="/role", tags=["roles"])


@router.post("/create", response_model=RoleResponse)
async def create_role(
    role_in: RoleCreate, service: RoleService = Depends(role_service)
):
    response = await service.create(role_in)
    return response
