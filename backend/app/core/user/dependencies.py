import logging

import jwt
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.schemas import TokenData
from app.core.security import get_secret_key, oauth2_schema
from app.core.user.model import User
from app.core.user.repository import UserRepository
from app.core.user.service import UserService

logger = logging.getLogger("USER_DEPS")


async def user_repository(  # noqa: F811
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    logger.debug("USER REPO INJECTED")
    return UserRepository(session)


async def user_service(
    repository: UserRepository = Depends(user_repository),
) -> UserService:
    logger.debug("USER SERVICE INJECTED")
    return UserService(repository)

async def get_current_user(
    token: str = Depends(oauth2_schema),
    repository: UserRepository = Depends(user_repository),
) -> User:
    try:
        secret_key = get_secret_key()
        payload = jwt.decode(token, secret_key, "HS256")
        user_id = payload.get("sub")
        token_data = TokenData(user_id=user_id)
        user = await repository.get_by_id(token_data.user_id)
        if user is None:
            raise ValueError
        return user

    except Exception as e:
        raise e
