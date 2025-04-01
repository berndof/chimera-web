import logging

from fastapi import APIRouter, Depends

from app.core.user.dependencies import user_service
from app.core.user.schemas import (
    UserBase,
    UserDetail,
    UserFilter,
    UserIn,
    UserPublic,
)
from app.core.user.service import UserService
from app.utils.pagination.dependencies import get_sorting_params
from app.utils.pagination.schemas import (
    PaginatedResponse,
    PaginationParams,
    SortingParams,
)

_logger = logging.getLogger("USER ROUTER")

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", response_model=UserDetail)
async def user_create(user_in: UserIn, service: UserService = Depends(user_service)):
    try:
        response = await service.create(user_in)
        return response
    except Exception as e:
        _logger.error(e)
        raise e


@router.post("/list", response_model=PaginatedResponse[UserBase])
async def user_list(
    service: UserService = Depends(user_service),
    pagination: PaginationParams = Depends(),
    sorting: SortingParams = Depends(
        get_sorting_params(
            ["username", "created_at", "updated_at", "first_name", "last_name"]
        )
    ),
    filters: UserFilter = Depends(),
):
    response = await service.get_list(
        response_schema=UserPublic,
        page=pagination.page,
        per_page=pagination.per_page,
        sort_by=sorting.sort_by,
        order=sorting.order,
        filters=filters,
    )
    _logger.info(f"User list response: {response}")
    return response
