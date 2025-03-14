import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError

from app.core.exceptions import InvalidCredentialsException
from app.core.schemas import TokenData
from app.core.security import get_secret_key, oauth2_schema
from app.core.service import AuthService
from app.user.dependencies import user_repository
from app.user.model import User
from app.user.repository import UserRepository


async def auth_service(
    repository: UserRepository = Depends(user_repository)
) -> AuthService:
    return AuthService(repository)

async def current_user(
    token:str = Depends(oauth2_schema),
    repository: UserRepository = Depends(user_repository)
) -> User:
    try:
        secret_key = get_secret_key()
        payload = jwt.decode(token, secret_key, "HS256")
        user_id = payload.get('sub')
        if user_id is None:
            raise InvalidCredentialsException()

        token_data = TokenData(user_id=user_id)

    except InvalidTokenError:
        raise InvalidCredentialsException()

    if token_data.user_id is None:
        raise InvalidCredentialsException()

    user = await repository.get_by_id(token_data.user_id)
    if user is None:
        raise InvalidCredentialsException()

    return user