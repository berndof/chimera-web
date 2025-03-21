import logging
from collections.abc import Sequence

from sqlalchemy import asc, desc, func
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

    async def get_list(
        self, page: int, per_page: int, sort_by: str, order: str
    ) -> Sequence[Role] | None:
        self.logger.debug(f"GETTING {per_page} ROLES, OF PAGE {page}")

        offset = (page - 1) * per_page

        count_total_query = select(func.count()).select_from(self.model)
        total_results = await self.session.execute(count_total_query)
        total = total_results.scalar_one()

        total_pages = (total + per_page - 1) // per_page

        if page > total_pages:
            return None

        #Ordenamento
        sort_column = getattr(self.model, sort_by)
        order_func = asc if order == "asc" else desc

        query = (
            select(self.model).
            order_by(order_func(sort_column)).
            offset(offset).limit(per_page)
        )
        result = await self.session.execute(query)
        items = result.scalars().all()

        final_result = {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "items": items
        }

        self.logger.debug("FINAL RESULT OF LIST QUERY")
        self.logger.debug(final_result)

        return final_result

