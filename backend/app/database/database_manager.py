import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database.exceptions import DbNotInitializedError


class DatabaseManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self.logger = logging.getLogger("DATABASE MANAGER")

        self._engine: AsyncEngine | None = create_async_engine(host, **engine_kwargs)
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = (
            async_sessionmaker(self._engine, class_=AsyncSession)
        )

    async def close(self) -> None:
        if not self._engine:
            raise DbNotInitializedError

        self.logger.info("Closing database connection...")
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
                self.logger.error(e)
                await conn.rollback()
                raise e

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self._sessionmaker:
            raise DbNotInitializedError()

        async with self._sessionmaker(expire_on_commit=False) as session:
            self.logger.debug("Opened new DB session")
            try:
                yield session
                await session.commit()
                self.logger.debug("Transaction committed successfully")
            except Exception as e:
                self.logger.error("Error during transaction, rolling back...", exc_info=True)
                await session.rollback()
                raise e
            finally:
                self.logger.debug("Closing DB session...")
                await session.close()

