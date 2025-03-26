from app.core.types import BaseRepository

from .models import Role
from .schemas import RoleIn


class RoleRepository(BaseRepository[Role]):
    async def create(self, role_in: RoleIn) -> Role:
        self.logger.debug(f"Creating role with data: {RoleIn}")
        try:
            new_role = Role(name=role_in.name, detail=role_in.detail)

            await self.save(new_role)
            return new_role
        except Exception as e:
            self.logger.error(e)
            raise e
