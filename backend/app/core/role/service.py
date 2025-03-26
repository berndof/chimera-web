from app.core.types import BaseSchema, BaseService

from .models import Role
from .repository import RoleRepository
from .schemas import RoleFilter, RoleIn


class RoleService(BaseService[Role, RoleRepository]):
    async def create(self, role_in: RoleIn) -> Role:
        # add user to default role
        return await self.repository.create(role_in)

    async def get_list(
        self,
        response_schema: BaseSchema[Role],
        page: int,
        per_page: int,
        sort_by: str,
        order: str,
        filters: RoleFilter,
    ):
        return await self.repository.get_list(
            response_schema, page, per_page, sort_by, order, filters
        )
