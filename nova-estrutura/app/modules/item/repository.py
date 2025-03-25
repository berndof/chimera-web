from app.core.repository import BaseRepository

from .models import Item


class ItemRepository(BaseRepository[Item]):
    async def get_by_name(self, name: str) -> str:
        return f"item {name}"
