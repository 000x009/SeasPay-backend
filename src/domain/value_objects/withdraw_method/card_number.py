from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.withdraw_method import CardNumberError


@dataclass(frozen=True)
class CardNumber(ValueObject[str]):
    value: str

    # def _validate(self) -> None:
    #     if not self.value.strip().isdigit() or len(self.value.strip()) != 16:
    #         raise CardNumberError("Card number must be 16 digits")
