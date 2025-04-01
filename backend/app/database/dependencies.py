
from os import getenv
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.database.database_manager import DatabaseManager


class Base(DeclarativeBase):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    __mapper_args__ = {"eager_defaults": True}


def get_database_url() -> str:
    db_data: dict[str, str] = {
        "host": getenv("POSTGRES_HOST", "postgres"),
        "port": getenv("POSTGRES_PORT", "5432"),
        "user": getenv("POSTGRES_USER", ""),
        "password": getenv("POSTGRES_PASSWORD", ""),
        "db_name": getenv("POSTGRES_DB", ""),
    }

    for key, value in db_data.items():
        if value == "":
            raise ValueError(
                f"Missing environment variable for Postgres connection: {key}"
            )

    return (
        f"postgresql+asyncpg://{db_data.get('user')}:{db_data.get('password')}"
        f"@{db_data.get('host')}:{db_data.get('port')}/{db_data.get('db_name')}"
    )


db_manager = DatabaseManager(get_database_url())
async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with db_manager.session() as session:
        yield session
