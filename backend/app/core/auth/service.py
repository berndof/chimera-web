from datetime import UTC, datetime, timedelta
from os import getenv
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status

from app.abs.service import BaseService
from app.core.auth.schemas import TokenData
from app.core.user.models import User
from app.core.user.repository import UserRepository
from app.utils.security import get_secret_key, oauth2_schema, validate_password


class AuthService(BaseService[UserRepository]):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repository.get_by("username", username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exists"
            )
        if not validate_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password"
            )
        return user

    def create_access_token(
        self, data: dict[str, Any], expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        env_expire_minutes = int(getenv("ACCESS_TOKEN_DURATION_MINUTES", 30))
        expire = datetime.now(UTC) + (expires_delta or timedelta(env_expire_minutes))
        to_encode.update({"exp": expire})
        secret_key = get_secret_key()
        return jwt.encode(to_encode, secret_key, algorithm="HS256")

    async def get_current_user(
        self,
        token: str = Depends(oauth2_schema),
    ) -> User:
        try:
            secret_key = get_secret_key()
            payload = jwt.decode(token, secret_key, "HS256")
            user_id = payload.get("sub")
            token_data = TokenData(user_id=user_id)
            user = await self.user_repository.get_by("id", token_data.user_id)
            return user

        except Exception as e:
            raise e
