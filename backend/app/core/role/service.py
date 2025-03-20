import logging

from app.core.role.exceptions import RoleAlreadyExists
from app.core.role.model import Role
from app.core.role.repository import RoleRepository
from app.core.role.schemas import RoleCreate


class RoleService:
    def __init__(self, repository: RoleRepository) -> None:
        self.repository: RoleRepository = repository
        self.logger = logging.getLogger("ROLE_SERVICE")

    async def create(self, role_in: RoleCreate) -> Role:
        role_exists: Role | None = await self.repository.get_by_name(role_in.name)

        if role_exists:
            raise RoleAlreadyExists()
        new_role: Role = await self.repository.create(role_in)
        return new_role

    async def get_by_name(self, name: str) -> Role | None:
        return await self.repository.get_by_name(name)
