import logging
from collections.abc import Sequence

from app.core.exceptions import EmptyPage
from app.core.role.exceptions import RoleAlreadyExists, RoleNotExists
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

    async def get_list(
        self, page: int, per_page: int, sort_by: str, order: str
    ) -> Sequence[Role]:
        items = await self.repository.get_list(page, per_page, sort_by, order)
        if items is None:
            raise EmptyPage()
        return items

    async def add_user(self, role_name):
        role: Role | None = await self.repository.get_by_name(role_name)
        if not role:
            raise RoleNotExists()


        #verificar se o user já faz parte do role

        try:
            await role.users.append()