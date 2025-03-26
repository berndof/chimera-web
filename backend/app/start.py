import logging
import os

from app.core.user import User, UserIn, UserRepository
from app.database.dependencies import get_db_session
from app.database.exceptions import DuplicateEntryError

logger = logging.getLogger("START")


async def start():
    superuser = await create_superuser()
    return superuser


async def create_superuser():
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
        logger.debug(f"Usuário duplicado: {e}")
