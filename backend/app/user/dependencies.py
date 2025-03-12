from fastapi import Depends

from app.core.database import get_db_session
from app.user.repository import UserRepository
from app.user.service import UserService


async def user_repository(session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)

async def user_service(repository = Depends(user_repository)) -> UserService:
    return UserService(repository)
