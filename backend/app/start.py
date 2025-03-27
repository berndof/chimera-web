import logging
import os

from app.database.dependencies import get_db_session
from app.database.exceptions import DuplicateEntryError

logger = logging.getLogger("START")


async def start() -> True:
    superuser = await create_superuser()
    superadmin_role = await create_superadmin_role()
    return


async def create_superuser():
    from app.core.user import User, UserIn, UserRepository

    async for session in get_db_session():
        user_repository = UserRepository(session, User)

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

    try:
        user_in = UserIn(**superuser_data)
        user = await user_repository.create(user_in)
        await session.commit()
        return user

    except DuplicateEntryError as e:
        logger.debug(e)
        pass


async def create_superadmin_role():
    from app.core.role import Role, RoleIn, RoleRepository

    async for session in get_db_session():
        role_repository = RoleRepository(session, Role)

        role_data: dict[str, str] = {
            "name": "super_admin",
            "detail": "default_superadmin_role",
        }
    try:
        role_in = RoleIn(**role_data)
        role = await role_repository.create(role_in)
        await session.commit()
        return role

    except DuplicateEntryError as e:
        logger.debug(e)
        pass
