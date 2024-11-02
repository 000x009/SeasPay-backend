from dataclasses import dataclass
from decimal import Decimal

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.platform_product import InvalidProductPriceError


@dataclass(frozen=True)
class Price(ValueObject[Decimal]):
    value: Decimal

    def _validate(self) -> None:
        if self.value <= 0:
            raise InvalidProductPriceError('The price must be greater than 0.')
