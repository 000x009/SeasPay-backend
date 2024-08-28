from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.completed_order import InvalidTakenCommissionError


@dataclass(frozen=True)
class TakenCommission(ValueObject[int]):
    value: int

    def _validate(self) -> None:
        if self.value < 0:
            raise InvalidTakenCommissionError('Value must be positive.')
