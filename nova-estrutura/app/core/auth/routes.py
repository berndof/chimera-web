from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.user import User, UserDetail

from .dependencies import auth_service, get_session_user
from .schemas import Token
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


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


@router.get("/me", response_model=UserDetail)
async def read_users_me(current_user: User = Depends(get_session_user)):
    return current_user
