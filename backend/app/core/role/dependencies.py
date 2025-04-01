import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.role.models import Role
from app.core.role.repository import RoleRepository
from app.core.role.service import RoleService
from app.database.dependencies import get_db_session

logger = logging.getLogger("ROLE_DEPS")


async def role_repository(
    session: AsyncSession = Depends(get_db_session),
) -> RoleRepository:
    logger.debug("ROLE REPO INJECTED")
    return RoleRepository(session, Role)


async def role_service(
    repository: RoleRepository = Depends(role_repository),
) -> RoleService:
    logger.debug("ROLE SERVICE INJECTED")
    return RoleService(repository)
