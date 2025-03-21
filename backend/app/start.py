# create default roles
# create superuser

import logging
import os

from app.core.database import get_db_session
from app.core.role import RoleRepository, RoleService
from app.core.role.exceptions import RoleAlreadyExists
from app.core.role.schemas import RoleCreate
from app.core.role.model import Role
from app.core.user import UserRepository, UserService
from app.core.user.exceptions import UserAlreadyExists
from app.core.user.schemas import UserCreate
from app.core.user.model import User

logger = logging.getLogger("START MODULE")

def get_default_superuser_user_data():
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
    return user_data

def get_default_superuser_role_data():
    role_data: dict[str, str] = {
        "name": "superuser",
        "description": "default superuser role"
    }
    return role_data


async def create_superuser_role() -> Role | None:
    async for session in get_db_session():  # Consumindo corretamente o gerador
        role_service = RoleService(RoleRepository(session))

        role_data = get_default_superuser_role_data()
        role_in = RoleCreate(
            name=role_data["name"],
            description=role_data["description"]
        )

        try:
            role = await role_service.create(role_in)
            await session.commit()
            return role
        except RoleAlreadyExists:
            return None


async def create_superuser_user():
    async for session in get_db_session():
        user_service = UserService(UserRepository(session))
        user_data = get_default_superuser_user_data()

        try:
            user_in = UserCreate(**user_data)  # type:ignore
            user = await user_service.create(user_in)
            await session.commit()
            return user
        except UserAlreadyExists:
            return None

async def add_superuser_to_role():
    async for session in get_db_session():  # Consumindo corretamente o gerador
        user_service = UserService(UserRepository(session))
        role_service = RoleService(RoleRepository(session))

        role_data = get_default_superuser_role_data()
        role = await role_service.get_by_name(role_data["name"])

        user_data = get_default_superuser_user_data()
        user = await user_service.get_by_username(user_data["username"])

        logger.debug(f"ROLE: {role}, USER: {user}")

