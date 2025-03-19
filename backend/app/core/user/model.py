from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.mixins import TimeStampMixin, UUIDMixin


class User(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(
        unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    detail: Mapped[str] = mapped_column(nullable=True)

    @property
    def full_name(self) -> str:
        return self.first_name + self.last_name
