import logging
from datetime import UTC, datetime, timedelta
from os import getenv
from typing import Any

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.schemas import Token
from app.core.security import get_secret_key, validate_password
from app.core.user import User, UserRepository
from app.core.user.dependencies import get_current_user, user_repository
from app.core.user.schemas import UserResponse

logger = logging.getLogger("AUTH")

router = APIRouter(prefix="/auth", tags=["auth"])

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repository.get_by_username(username)
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

async def auth_service(
    repository: UserRepository = Depends(user_repository),
) -> AuthService:
    return AuthService(repository)

@router.post("/token", response_model=Token)
async def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(auth_service),
):
    user: User = await auth_service.authenticate_user(
        form_data.username, form_data.password
    )

    # Changing expire delta
    # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = auth_service.create_access_token(data={"sub": user.username},
    # expires_delta=access_token_expires)

    access_token: str = auth_service.create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    logger.debug(current_user.roles)
    return current_user
