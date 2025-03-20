import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.role.model import Role
from app.core.role.schemas import RoleCreate


class RoleRepository:
    def __init__(
        self,
        database_session: AsyncSession,
    ) -> None:
        self.session: AsyncSession = database_session
        self.model = Role
        self.logger = logging.getLogger("ROLE_REPOSITORY")

    async def create(self, role_in: RoleCreate) -> Role:
        self.logger.debug(f"CREATING NEW ROLE, role_in: {role_in}")
        new_role = Role(name=role_in.name, description=role_in.description)
        self.session.add(new_role)
        await self.session.flush()
        await self.session.refresh(new_role)
        return new_role

    async def get_by_name(self, name: str) -> Role | None:
        self.logger.debug(f"FINDING ROLE BY NAME {name}")
        selection_query = select(self.model).where(self.model.name == name)
        result = await self.session.execute(selection_query)
        role: Role | None = result.scalar_one_or_none()
        self.logger.debug(f"FINDED ROLE {role}")
        return role
