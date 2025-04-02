from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class SoftDeleteMixin:
    """
    Mixin para Soft Delete.

    - A coluna `deleted_at` armazena a data/hora em que o registro foi marcado como deletado.
      Se for `None`, o registro está ativo.
    - O método `soft_delete` marca o registro como deletado sem removê-lo do banco.
    - O método `restore` restaura o registro para o estado ativo.
    - O método de classe `filter_active` pode ser usado para filtrar registros ativos.
    """
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def soft_delete(self) -> None:
        """
        Realiza o soft delete do registro.
        Em vez de remover, atualiza a coluna `deleted_at` com o timestamp atual.
        """
        self.deleted_at = func.now()
        return

    def restore(self) -> None:
        """
        Restaura o registro previamente marcado como deletado.
        """
        self.deleted_at = None

    @property
    def is_active(self) -> bool:
        """
        Verifica se o registro está ativo (não deletado).
        """
        return self.deleted_at is None

    @classmethod
    def filter_active(cls, query):
        """
        Adiciona um filtro para retornar apenas os registros ativos (não deletados).
        """
        return query.filter(cls.deleted_at.is_(None))
