import logging
import os
from typing import TYPE_CHECKING

from app.core.role import Role, RoleIn, RoleRepository
from app.core.user import User, UserIn, UserRepository
from app.database.dependencies import get_db_session
from app.database.exceptions import DuplicateEntryError

logger = logging.getLogger("START")


def get_defaults():
    superuser_data: dict[str, str | None] = {
        "username": os.getenv("SUPERUSER_USERNAME"),
        "email": os.getenv("SUPERUSER_EMAIL", None),
        "first_name": os.getenv("SUPERUSER_FIRSTNAME", "Super"),
        "last_name": os.getenv("SUPERUSER_LASTNAME", "User"),
        "password": os.getenv("SUPERUSER_PASSWORD"),
    }

    missing_keys = [
        key for key, value in superuser_data.items() if value is None and not "email"
    ]

    if missing_keys:
        raise ValueError(f"Variáveis de ambiente ausentes: {', '.join(missing_keys)}")

    role_data: dict[str, str] = {
        "name": "super_admin",
        "detail": "default_superadmin_role",
    }

    return superuser_data, role_data


superuser_data, superadmin_role_data = get_defaults()


async def start() -> True:
    superuser = await create_superuser()
    superadmin_role = await create_superadmin_role()
    await add_user_to_role(superuser, superadmin_role)
    return


async def add_user_to_role(user: User, role: Role):
    async for session in get_db_session():
        role_repository = RoleRepository(session, Role)
        try:
            await role_repository.add_user_to_role(user, role)
            await session.commit()
        except Exception as e:
            logger.error(f"TRATAR AQUI TAMBEM {e}")
            raise e
        return


async def create_superuser() -> User:
    try:
        async for session in get_db_session():
            user_repository = UserRepository(session, User)
            user_in = UserIn(**superuser_data)
            user = await user_repository.create(user_in)
            await session.commit()

    except DuplicateEntryError as e:
        logger.debug(e)
        async for session in get_db_session():  # Start a new session
            try:
                user_repository = UserRepository(session, User)
                user = await user_repository.get_by("username", user_in.username)
            except Exception as e:
                logger.error(f"Fugiu do esperado {e}")
                raise e
    return user


async def create_superadmin_role() -> Role:
    try:
        async for session in get_db_session():
            role_repository = RoleRepository(session, Role)
            role_in = RoleIn(**superadmin_role_data)
            role = await role_repository.get_by(field="name", value=role_in.name)
            await session.commit()

    except DuplicateEntryError as e:
        logger.debug(e)
        async for session in get_db_session():  # Start a new session
            try:
                role_repository = RoleRepository(session, Role)
                role = await role_repository.get_by_name(role_in.name)
            except Exception as e:
                logger.error(f"Fugiu do esperado {e}")
                raise e
    return role
