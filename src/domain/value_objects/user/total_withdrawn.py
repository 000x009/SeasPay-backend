from decimal import Decimal

from src.domain.common.value_objects import ValueObject


class TotalWithdrawn(ValueObject[Decimal]):
    value: Decimal
