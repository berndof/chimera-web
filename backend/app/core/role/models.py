from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.dependencies import SQLBaseModel

if TYPE_CHECKING:
    from app.core.user.models import User


class Role(SQLBaseModel):
    __tablename__: str = "role"

    name: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    detail: Mapped[str] = mapped_column(nullable=True)

    users: Mapped[list[User]] = relationship(
        "User", secondary="user_roles", back_populates="roles", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}', '{self.detail}')>"
