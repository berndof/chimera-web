import logging

from fastapi import APIRouter, Depends

from app.core.pagination import PaginationParams, SortingParams, get_sorting_params
from app.core.types import PaginatedResponse

from app.core.role.dependencies import role_service
from app.core.role.schemas import RoleBase, RoleFilter, RoleIn
from app.core.role.service import RoleService

_logger = logging.getLogger("ROLE ROUTER")

router = APIRouter(prefix="/role", tags=["role"])


@router.post("/create", response_model=RoleBase)
async def user_create(role_in: RoleIn, service: RoleService = Depends(role_service)):
    try:
        response = await service.create(role_in)
        return response
    except Exception as e:
        _logger.error(e)
        raise e


@router.post("/list", response_model=PaginatedResponse[RoleBase])
async def user_list(
    service: RoleService = Depends(role_service),
    pagination: PaginationParams = Depends(),
    sorting: SortingParams = Depends(
        get_sorting_params(["name", "created_at", "updated_at"])
    ),
    filters: RoleFilter = Depends(),
):
    response = await service.get_list(
        response_schema=RoleBase,
        page=pagination.page,
        per_page=pagination.per_page,
        sort_by=sorting.sort_by,
        order=sorting.order,
        filters=filters,
    )
    _logger.info(f"User list response: {response}")
    return response
