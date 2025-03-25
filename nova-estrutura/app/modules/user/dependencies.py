import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session

from .models import User
from .repository import UserRepository
from .service import UserService

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
