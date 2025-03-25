import logging

from fastapi import APIRouter, Depends, Query
from app.core.role.exceptions import UserAlreadyInRole

from app.core.role.dependencies import role_service
from app.core.role.schemas import RoleCreate, RoleResponse, RoleUserAdd, RoleDetail
from app.core.role.service import RoleService
from app.core.schemas import ListResponse
from app.core.user.dependencies import user_service
from app.core.user.service import UserService

logger = logging.getLogger("ROLE_ROUTES")

all: list[str] = ["router"]
router = APIRouter(prefix="/role", tags=["roles"])


@router.post("/create", response_model=RoleResponse)
async def create_role(
    role_in: RoleCreate, service: RoleService = Depends(role_service)
):
    response = await service.create(role_in)
    return response


@router.get("/list", response_model=ListResponse[RoleResponse])
async def get_list(
    service: RoleService = Depends(role_service),
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(10, ge=1, le=100, description="Registros por página"),
    sort_by: str = Query("name", regex="^(name|created_at)$", descripton="Ordenar por"),
    # TODO adicionar mais métodos de ordenamento
    order: str = Query("asc", regex="^(asc|desc)$", description="Ordem"),
):
    # adicionar validação de papel de usuário
    # antes de definir o tipo de schema de resposta
    # TODO FUTURE criar um decorador para analisar a permissão automaticamente
    response = await service.get_list(
        page=page, per_page=per_page, sort_by=sort_by, order=order
    )
    return response


@router.post(
    "/add_user",
    response_model=RoleDetail,
)
async def add_user(
    role_user_in: RoleUserAdd,
    role_service: RoleService = Depends(role_service),
    user_service: UserService = Depends(user_service),
):
    logger.debug(f"ADICIONAR USER A UM ROLE, DATA: {role_user_in}")

    # tenta coletar o role
    role = await role_service.get_by_name(role_user_in.role_name)
    # tenta coletar o user
    user = await user_service.get_by_username(role_user_in.username)

    if user in role.users:
        raise UserAlreadyInRole()

    return await role_service.add_user_to_role(role, user)
