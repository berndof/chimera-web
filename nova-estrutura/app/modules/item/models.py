from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Item(Base):
    __tablename__: str = "item"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, unique=True, autoincrement=True
    )

    name: Mapped[str] = mapped_column(index=True, nullable=False, unique=True)

    description: Mapped[str] = mapped_column(nullable=True)
