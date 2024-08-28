from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class CompletedOrderID(ValueObject[int]):
    value: int
