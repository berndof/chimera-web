import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session

from .models import Item
from .repository import ItemRepository
from .service import ItemService


async def item_repository(  # noqa: F811
    session: AsyncSession = Depends(get_db_session),
) -> ItemRepository:
    return ItemRepository(session, Item)


async def item_service(
    repository: ItemRepository = Depends(item_repository),
) -> ItemService:
    return ItemService(repository)
