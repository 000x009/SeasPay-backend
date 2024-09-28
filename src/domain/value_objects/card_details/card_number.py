from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.card_details import CardNumberError


@dataclass(frozen=True)
class CardNumber(ValueObject[int]):
    value: int

    def _validate(self) -> None:
        if self.value < 1000000000000000 or self.value > 9999999999999999:
            raise CardNumberError("Card number must be 16 digits")
