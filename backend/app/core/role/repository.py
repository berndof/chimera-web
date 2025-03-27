from __future__ import annotations
from sqlalchemy.exc import IntegrityError

from app.core.types import BaseRepository
from app.database.exceptions import DuplicateEntryError, RelationAlreadyExistsError

from .models import Role
from .schemas import RoleIn

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.user import User


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

        self.logger.info(role.users)
        self.logger.info(user)

        if any(existing_user.id == user.id for existing_user in role.users):
            self.logger.debug("User already in role skipping")
            raise RelationAlreadyExistsError([User, Role])
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
