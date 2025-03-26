import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.pagination import PaginationParams, SortingParams, get_sorting_params
from app.core.types import PaginatedResponse

from .dependencies import user_service
from .schemas import UserBase, UserDetail, UserIn, UserFilter, UserPublic
from .service import UserService

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


""" @router.get("/list", response_model=ListResponse[UserBase])
async def user_list(
    service: UserService = Depends(user_service),
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(10, ge=1, le=100, description="Registros por página"),
    sort_by: str = Query(
        "username", regex="^(username|created_at)$", descripton="Ordenar por"
    ),
    order: str = Query("asc", regex="^(asc|desc)$", description="Ordem"),
):
    response = await service.get_list(
        page=page, per_page=per_page, sort_by=sort_by, order=order
    )
    return response """


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
