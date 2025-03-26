from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from app.database.dependencies import Base
from app.database.mixins import TimeStampMixin, UUIDMixin


class Role(Base, UUIDMixin, TimeStampMixin):
    __tablename__: str = "role"

    name: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    detail: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}', '{self.detail}')>"
