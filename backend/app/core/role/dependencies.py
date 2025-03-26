import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db_session

from .models import Role
from .repository import RoleRepository
from .service import RoleService

logger = logging.getLogger("ROLE_DEPS")


async def role_repository(  # noqa: F811
    session: AsyncSession = Depends(get_db_session),
) -> RoleRepository:
    logger.debug("ROLE REPO INJECTED")
    return RoleRepository(session, Role)


async def role_service(
    repository: RoleRepository = Depends(role_repository),
) -> RoleService:
    logger.debug("USER SERVICE INJECTED")
    return RoleService(repository)
