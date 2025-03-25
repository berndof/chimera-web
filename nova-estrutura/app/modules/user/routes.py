import logging

from fastapi import APIRouter, Depends

from .dependencies import user_service
from .schemas import UserDetail, UserIn
from .service import UserService

_logger = logging.getLogger("USER ROUTER")

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", response_model=UserDetail)
async def item_create(user_in: UserIn, service: UserService = Depends(user_service)):
    try:
        response = await service.create(user_in)
        return response
    except Exception as e:
        _logger.error(e)
        raise e
