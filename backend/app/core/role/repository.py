from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from app.core.role.models import Role
from app.core.role.schemas import RoleIn
from app.database.exceptions import DuplicateEntryError, RelationAlreadyExistsError
from app.types.repository import BaseRepository

if TYPE_CHECKING:
    from app.core.user.models import User


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

    async def add_user_to_role(self, user: User, role: Role) -> Role:
        self.logger.debug(f"Adding user {user.id} to role {role.id}")

        if any(existing_user.id == user.id for existing_user in role.users):
            self.logger.debug("raising Relation Already Exists")
            raise RelationAlreadyExistsError([user, role])
        else:
            try:
                role.users.append(user)
                self.logger.debug(f"User {user.id} appended to role {role.id}")
                await self.save(role)
                self.logger.debug(f"Role {role.id} saved with user {user.id}")
                return role
            except Exception as e:
                self.logger.error(
                    f"Error while adding user {user.id} to role {role.id}: {e}"
                )
                raise
