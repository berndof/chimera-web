from collections.abc import Callable
from operator import and_
from typing import Any

from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import BinaryExpression


class Operators:
    """Classe que encapsula operadores para filtros SQLAlchemy."""

    @staticmethod
    def eq(column: InstrumentedAttribute[Any], value: Any) -> BinaryExpression[Any]:
        """Igualdade."""
        return column == value

    @staticmethod
    def neq(column: InstrumentedAttribute[Any], value: Any) -> BinaryExpression[Any]:
        """Diferente."""
        return column != value

    @staticmethod
    def contains(
        column: InstrumentedAttribute[Any], value: str
    ) -> BinaryExpression[Any]:
        """Contém (case insensitive)."""
        return column.ilike(f"%{value}%")

    @staticmethod
    def not_contains(
        column: InstrumentedAttribute[Any], value: str
    ) -> BinaryExpression[Any]:
        """Não contém (case insensitive)."""
        return ~column.ilike(f"%{value}%")

    @staticmethod
    def gt(column: InstrumentedAttribute[Any], value: Any) -> BinaryExpression[Any]:
        """Maior que."""
        return column > value

    @staticmethod
    def lt(column: InstrumentedAttribute[Any], value: Any) -> BinaryExpression[Any]:
        """Menor que."""
        return column < value

# Mapeamento de operadores com tipagem corrigida
OPERATORS: dict[
    str, Callable[[InstrumentedAttribute[Any], Any], BinaryExpression[Any]]
] = {
    "eq": Operators.eq,
    "neq": Operators.neq,
    "contains": Operators.contains,
    "not_contains": Operators.not_contains,
    "gt": Operators.gt,
    "lt": Operators.lt,
}


class FilterableMixin:
    """
    Mixin que adiciona um método para aplicar filtros dinâmicos
    à query de um modelo SQLAlchemy.
    """
    @classmethod
    def apply_filters(
        cls, query: Select, filters: dict[str, dict[str, Any]]
    ) -> Select:
        conditions: list[BinaryExpression] = []

        # Se a classe possuir o mixin de soft delete,
        # adiciona o filtro para registros ativos
        if hasattr(cls, "deleted_at"):
            conditions.append(cls.deleted_at.is_(None))

        for field, rule in filters.items():
            # Verifica se o campo existe no modelo e se o valor foi definido
            if hasattr(cls, field):
                value = rule.get("value")
                if value is not None:
                    operator_name = rule.get("operator", "eq")
                    operator_func = OPERATORS.get(operator_name)
                    if operator_func:
                        column = getattr(cls, field)
                        conditions.append(operator_func(column, value))

        if conditions:
            query = query.where(and_(*conditions))
        return query
