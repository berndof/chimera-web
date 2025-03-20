import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash
from app.core.user.schemas import UserCreate
from app.models import User


class UserRepository:
    def __init__(
        self,
        database_session: AsyncSession,
    ) -> None:
        self.session: AsyncSession = database_session
        self.model = User
        self.logger = logging.getLogger("USER_REPOSITORY")

    async def create(self, user_in: UserCreate) -> User:
        new_user = User(
            username=user_in.username,
            email=user_in.email,
            password=get_password_hash(user_in.password),
            first_name=user_in.first_name,
            last_name=user_in.last_name,
        )
        self.session.add(new_user)
        await self.session.flush()
        await self.session.refresh(new_user)
        return new_user

    async def get_by_username(self, username: str) -> User | None:
        self.logger.debug(f"FINDING USER BY USERNAME {username}")
        selection_query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(selection_query)
        user: User | None = result.scalar_one_or_none()
        self.logger.debug(f"FINDED USER {user}")
        return user

    async def get_by_id(self, user_id: str) -> User | None:
        self.logger.debug(f"FINDING USER BY ID {user_id}")
        selection_query = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(selection_query)
        user: User | None = result.scalar_one_or_none()
        self.logger.debug(f"FINDED USER {user}")
        return user
