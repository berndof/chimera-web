from app.core.service import BaseService
from app.modules.item.models import Item

from .repository import ItemRepository


class ItemService(BaseService[Item, ItemRepository]):
    async def get_by_name(self, name: str) -> str:
        return await self.repository.get_by_name(name)
