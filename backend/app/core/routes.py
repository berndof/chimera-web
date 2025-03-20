from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import auth_service, current_user, health_service
from app.core.schemas import HealthResponse, Token
from app.core.service import AuthService, HealthService
from app.core.user.schemas import UserResponse
from app.models import User

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/auth/token", response_model=Token)
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


@auth_router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(current_user)):
    return current_user


health_router = APIRouter(tags=["health"])


@health_router.get("/health", response_model=HealthResponse)
async def health(health_service: HealthService = Depends(health_service)):
    return await health_service.check_health()
