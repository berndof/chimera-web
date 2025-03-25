import logging
from typing import TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.role.exceptions import RolePermissionDenied
from app.core.role.service import Role
from app.core.user.dependencies import get_current_user
from app.core.user.model import User

logger = logging.getLogger("ROLE_DEPS")


async def role_repository(
    session: AsyncSession = Depends(get_db_session),
) -> RoleRepository:
    logger.debug("ROLE REPO INJECTED")
    return RoleRepository(session)


async def role_service(
    repository: RoleRepository = Depends(role_repository),
) -> RoleService:
    logger.debug("ROLE SERVICE INJECTED")
    return RoleService(repository)


def require_role(required_roles: list[str]):
    async def role_dependency(current_user: User = Depends(get_current_user)):
        user_roles = {role.name for role in current_user.roles}

        for role in required_roles:
            if role in user_roles:
                return role

        raise RolePermissionDenied()

    return role_dependency
