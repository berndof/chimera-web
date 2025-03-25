from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, db_session: AsyncSession, model: type[T]):
        self.db_session = db_session
        self.model = model

    async def save(self, obj: T) -> None:
        self.db_session.add(obj)
        await self.db_session.flush()
        await self.db_session.refresh(obj)
