import logging
from collections.abc import Sequence

from fastapi import HTTPException, status

from app.core.exceptions import EmptyPage
from app.core.role.exceptions import RoleAlreadyExists, RoleNotExists
from app.core.role.model import Role
from app.core.role.repository import RoleRepository
from app.core.role.schemas import RoleCreate
from app.core.user.model import User


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

    async def get_by_name(self, name: str) -> Role:
        role = await self.repository.get_by_name(name)
        if role is None:
            raise RoleNotExists()
        return role

    async def get_list(
        self, page: int, per_page: int, sort_by: str, order: str
    ) -> Sequence[Role]:
        items = await self.repository.get_list(page, per_page, sort_by, order)
        if items is None:
            raise EmptyPage()
        return items

    async def add_user_to_role(self, _role: Role, user: User):
        role = await self.repository.add_user_to_role(_role, user)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"error adding user {user.username} to role {_role.name}",
            )
        return role
