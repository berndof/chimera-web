import logging

from fastapi import Depends

from app.core.security import oauth2_schema
from app.core.user.dependencies import UserRepository, user_repository

from .service import AuthService

logger = logging.getLogger("USER_DEPS")


async def auth_service(
    repository: UserRepository = Depends(user_repository),
) -> AuthService:
    logger.debug("USER SERVICE INJECTED")
    return AuthService(repository)


async def get_session_user(
    token: str = Depends(oauth2_schema), service: AuthService = Depends(auth_service)
):
    return await service.get_current_user(token)
