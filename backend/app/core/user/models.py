from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.dependencies import Base
from app.database.mixins import TimeStampMixin, UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.role import Role

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id", ForeignKey(column="user.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "role_id", ForeignKey(column="role.id", ondelete="CASCADE"), primary_key=True
    ),
)


class User(Base, UUIDMixin, TimeStampMixin):
    __tablename__: str = "user"

    username: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    detail: Mapped[str] = mapped_column(nullable=True)

    roles: Mapped[list[Role]] = relationship(
        "Role", secondary="user_roles", back_populates="users", lazy="selectin"
    )

    @property
    def full_name(self) -> str:
        return self.first_name + self.last_name

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, username='{self.username}', "
            f"fullname='{self.full_name}', email='{self.email}')>"
        )
