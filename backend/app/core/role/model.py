from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.mixins import TimeStampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models import User


class Role(Base, UUIDMixin, TimeStampMixin):
    __tablename__: str = "role"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    users: Mapped[list["User"]] = relationship(
        secondary="user_roles",
        back_populates="roles",
    )
