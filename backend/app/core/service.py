from datetime import UTC, datetime, timedelta
from os import getenv
from typing import Any

import jwt

from app.core.exceptions import InvalidCredentialsException
from app.core.security import get_secret_key, validate_password
from app.user.model import User
from app.user.repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repository.get_by_username(username)
        if not user:
            raise InvalidCredentialsException(detail="User Not Found")
        if not validate_password(password, user.password):
            raise InvalidCredentialsException(detail="Invalid Password")
        return user

    def create_access_token(
        self, data: dict[str, Any], expires_delta: timedelta | None = None
    ):
        to_encode = data.copy()
        env_expire_minutes = int(getenv("ACCESS_TOKEN_DURATION_MINUTES", 30))
        expire = datetime.now(UTC) + (expires_delta or timedelta(env_expire_minutes))
        to_encode.update({"exp": expire})
        secret_key = get_secret_key()
        return jwt.encode(to_encode, secret_key, algorithm="HS256")
