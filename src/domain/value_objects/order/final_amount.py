from decimal import Decimal
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class FinalAmount(ValueObject[Decimal]):
    value: Decimal
