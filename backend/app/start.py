__all__ = ["start"]

import logging
import os

from app.core.role.models import Role
from app.core.role.repository import RoleRepository
from app.core.role.schemas import RoleIn
from app.core.user.models import User
from app.core.user.repository import UserRepository
from app.core.user.schemas import UserIn
from app.database.dependencies import get_db_session
from app.database.exceptions import DuplicateEntryError, RelationAlreadyExistsError

logger = logging.getLogger("START")


def get_superuser_default() -> dict[str, str]:
    superuser_data: dict[str, str] = {
        "username": os.getenv("SUPERUSER_USERNAME", ""),
        "email": os.getenv("SUPERUSER_EMAIL", ""),
        "first_name": os.getenv("SUPERUSER_FIRSTNAME", "Super"),
        "last_name": os.getenv("SUPERUSER_LASTNAME", "User"),
        "password": os.getenv("SUPERUSER_PASSWORD", ""),
    }

    if superuser_data["email"] == "":
        superuser_data.pop("email")

    missing_keys = [
        key for key, value in superuser_data.items() if value == ""
    ]


    if missing_keys:
        raise ValueError(f"Variáveis de ambiente ausentes: {', '.join(missing_keys)}")

    return superuser_data

def get_superadmin_role_default() -> dict[str, str]:
    role_data: dict[str, str] = {
        "name": "super_admin",
        "detail": "default_superadmin_role",
    }
    return role_data

superuser_data = get_superuser_default()
super_admin_role_data = get_superadmin_role_default()

async def start():
    superuser = await create_superuser()
    superadmin_role = await create_superadmin_role()
    if superuser is None or superadmin_role is None:
        logger.error("Superuser or superadmin role creation failed.")
        raise ValueError(
            "Superuser or superadmin role creation failed. Check logs for details."
        )
    await add_user_to_role(superuser, superadmin_role)
    return

async def add_user_to_role(user: User, role: Role):
    async for session in get_db_session():
        role_repository = RoleRepository(session, Role)
        try:
            await role_repository.add_user_to_role(user, role)
            await session.commit()
        except RelationAlreadyExistsError as rae:
            logger.debug(rae)
            pass

async def create_superuser() -> User:
    user_in = UserIn(**superuser_data)
    try:
        async for session in get_db_session():
            user_repository = UserRepository(session, User)
            user = await user_repository.create(user_in)
            await user_repository.save(obj=user)

    except DuplicateEntryError as e:
        logger.debug(e)

        async for session in get_db_session():  # Start a new session
            try:
                user_repository = UserRepository(session, User)
                user = await user_repository.get_by("username", user_in.username)

            except Exception as e:
                logger.error(f"Error on superuser creation {e}")
                raise e
    return user

async def create_superadmin_role() -> Role | None:
    role_in = RoleIn(**super_admin_role_data)
    try:
        async for session in get_db_session():
            role_repository = RoleRepository(session, Role)
            role_in = RoleIn(**super_admin_role_data)
            role = await role_repository.create(role_in)
            await session.commit()

    except DuplicateEntryError as e:
        logger.debug(e)
        async for session in get_db_session():  # Start a new session
            try:
                role_repository = RoleRepository(session, Role)
                role = await role_repository.get_by("name", role_in.name)
            except Exception as e:
                logger.error(f"Error on superadmin role creation {e}")
                raise e
    return role
