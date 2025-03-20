import jwt
from fastapi import Depends

from app.core.schemas import TokenData
from app.core.security import get_secret_key, oauth2_schema
from app.core.service import AuthService, HealthService
from app.core.user.dependencies import user_repository
from app.core.user.repository import UserRepository
from app.models import User


async def auth_service(
    repository: UserRepository = Depends(user_repository),
) -> AuthService:
    return AuthService(repository)


async def current_user(
    token: str = Depends(oauth2_schema),
    repository: UserRepository = Depends(user_repository),
) -> User:
    try:
        secret_key = get_secret_key()
        payload = jwt.decode(token, secret_key, "HS256")
        user_id = payload.get("sub")
        token_data = TokenData(user_id=user_id)
        user = await repository.get_by_id(token_data.user_id)
        return user

    except Exception as e:
        raise e


async def health_service():
    return HealthService()
