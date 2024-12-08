from decimal import Decimal

from src.domain.common.value_objects import ValueObject


class PaidAmount(ValueObject[Decimal]):
    value: Decimal
