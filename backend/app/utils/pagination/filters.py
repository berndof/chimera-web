
from collections.abc import Callable
from typing import Any

from sqlalchemy.orm.attributes import InstrumentedAttribute
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
