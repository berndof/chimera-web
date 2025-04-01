import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user.models import User
from app.core.user.repository import UserRepository
from app.core.user.service import UserService
from app.database.dependencies import get_db_session

logger = logging.getLogger("USER_DEPS")


async def user_repository(  # noqa: F811
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    logger.debug("USER REPO INJECTED")
    return UserRepository(session, User)


async def user_service(
    repository: UserRepository = Depends(user_repository),
) -> UserService:
    logger.debug("USER SERVICE INJECTED")
    return UserService(repository)
