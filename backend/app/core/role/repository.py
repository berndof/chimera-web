from sqlalchemy.exc import IntegrityError

from app.core.types import BaseRepository
from app.database.exceptions import DuplicateEntryError

from .models import Role
from .schemas import RoleIn


class RoleRepository(BaseRepository[Role]):
    async def create(self, role_in: RoleIn) -> Role:
        self.logger.debug(f"Creating role with data: {RoleIn}")
        try:
            new_role = Role(name=role_in.name, detail=role_in.detail)

            await self.save(new_role)
            return new_role
        except IntegrityError as ie:
            if "ix_role_name" in str(ie.orig):
                raise DuplicateEntryError(Role)
            raise ie
