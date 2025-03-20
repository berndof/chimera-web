import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.user.repository import UserRepository
from app.core.user.service import UserService

logger = logging.getLogger("USER_DEPS")


async def user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    logger.debug("USER REPO INJECTED")
    return UserRepository(session)


async def user_service(
    repository: UserRepository = Depends(user_repository),
) -> UserService:
    logger.debug("USER SERVICE INJECTED")
    return UserService(repository)
