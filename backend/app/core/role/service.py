from app.core.role.models import Role
from app.core.role.repository import RoleRepository
from app.core.role.schemas import RoleIn
from app.types.service import BaseService


class RoleService(BaseService[RoleRepository]):
    async def create(self, role_in: RoleIn) -> Role:
        # add user to default role
        return await self.repository.create(role_in)


