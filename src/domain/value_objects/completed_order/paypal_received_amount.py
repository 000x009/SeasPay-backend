from dataclasses import dataclass
from decimal import Decimal

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.completed_order import InvalidUserReceivedAmountError


@dataclass(frozen=True)
class PaypalReceivedAmount(ValueObject[Decimal]):
    value: Decimal

    def _validate(self) -> None:
        if self.value <= 0:
            raise InvalidUserReceivedAmountError('Value must be greater than zero.')