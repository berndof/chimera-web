import logging
from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager
from os import getenv
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.exceptions import DbNotInitializedError

logger = logging.getLogger("DATABASE MANAGER")
logger.setLevel(logging.DEBUG)


class Base(DeclarativeBase):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    __mapper_args__ = {"eager_defaults": True}


class DatabaseManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}

        self._engine: AsyncEngine | None = create_async_engine(host, **engine_kwargs)
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = (
            async_sessionmaker(self._engine, class_=AsyncSession)
        )

    async def close(self) -> None:
        if not self._engine:
            raise DbNotInitializedError

        logger.info("Closing database connection...")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if not self._engine:
            raise DbNotInitializedError

        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception as e:
                logger.error(e)
                await conn.rollback()
                raise e

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self._sessionmaker:
            raise DbNotInitializedError()

        async with self._sessionmaker() as session:
            logger.debug("Opened new DB session")
            try:
                yield session
                await session.commit()
                logger.debug("Transaction committed successfully")
            except Exception as e:
                logger.error("Error during transaction, rolling back...", exc_info=True)
                await session.rollback()
                raise e
            finally:
                logger.debug("Closing DB session...")
                await session.close()


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

    return f"postgresql+asyncpg://{db_data.get('user')}:{db_data.get('password')}@{db_data.get('host')}:{db_data.get('port')}/{db_data.get('db_name')}"


db_manager = DatabaseManager(get_database_url())


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with db_manager.session() as session:
        yield session
