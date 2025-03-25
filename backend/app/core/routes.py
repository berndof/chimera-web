"""from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import auth_service, current_user, health_service
from app.core.schemas import HealthResponse, Token
from app.core.service import AuthService, HealthService
from app.core.user import User
from app.core.user.schemas import UserResponse

router = APIRouter()


@router.get(
    "/dashboard", response_model=Union[AdminResponse, ManagerResponse, UserResponse]
)
async def dashboard(role: str = Depends(require_role(["admin", "manager", "user"]))):
    if role == "admin":
        return AdminResponse(
            message="Bem-vindo ao painel de administração!",
            full_access=True,
            managed_users=["user1", "user2", "user3"],
        )
    elif role == "manager":
        return ManagerResponse(
            message="Bem-vindo ao painel de gerência!",
            department="Vendas",
            team_size=10,
        )
    else:  # "user"
        return UserResponse(
            message="Bem-vindo ao painel do usuário!",
            profile_complete=True,
        )
"""
