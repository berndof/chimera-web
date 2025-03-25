from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.mixins import TimeStampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.core.user import User


class Role(Base, UUIDMixin, TimeStampMixin):
    __tablename__: str = "role"

    name: Mapped[str] = mapped_column(index=True, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    users: Mapped[list[User]] = relationship(
        "User", secondary="user_roles", back_populates="roles", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}', description='{self.description}')>"
