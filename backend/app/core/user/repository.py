from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash
from app.core.user.model import User
from app.core.user.schemas import UserCreate


class UserRepository:
    def __init__(
        self,
        database_session: AsyncSession,
    ):
        self.session = database_session
        self.model = User

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

    async def get_by_username(self, username: str) -> User:
        selection_query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(selection_query)
        user = result.scalar_one_or_none()
        if user is None:
            raise KeyError("user dosnt exists")

    async def get_by_id(self, user_id: str) -> User:
        selection_query = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(selection_query)
        user = result.scalar_one_or_none()
        if user is None:
            raise ValueError("User dosnt exists")
        return user
