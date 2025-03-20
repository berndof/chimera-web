# create default roles
# create superuser

import logging
import os

from app.core.database import get_db_session
from app.core.role import RoleRepository, RoleService
from app.core.role.exceptions import RoleAlreadyExists
from app.core.role.schemas import RoleCreate
from app.core.user import UserRepository, UserService
from app.core.user.exceptions import UserAlreadyExists
from app.core.user.schemas import UserCreate

logger = logging.getLogger("START MODULE")


async def create_superuser_role():
    async for session in get_db_session():  # Consumindo corretamente o gerador
        role_service = RoleService(RoleRepository(session))
        role_in = RoleCreate(name="superuser", description="default superuser role")

        try:
            role = await role_service.create(role_in)
            await session.commit()
            return role
        except RoleAlreadyExists:
            return None


async def create_superuser_user():
    async for session in get_db_session():
        user_service = UserService(UserRepository(session))
        user_data: dict[str, str | None] = {
            "username": os.getenv("SUPERUSER_USERNAME"),
            "email": os.getenv("SUPERUSER_EMAIL", ""),
            "first_name": os.getenv("SUPERUSER_FIRSTNAME", "Super"),
            "last_name": os.getenv("SUPERUSER_LASTNAME", "User"),
            "password": os.getenv("SUPERUSER_PASSWORD"),
        }

        missing_keys = [key for key, value in user_data.items() if value is None]

        if missing_keys:
            raise ValueError(
                f"Variáveis de ambiente ausentes: {', '.join(missing_keys)}"
            )

        try:
            user_in = UserCreate(**user_data)  # type:ignore
            user = await user_service.create(user_in)
            await session.commit()
            return user
        except UserAlreadyExists:
            return None


async def add_superuser_to_role(): ...
