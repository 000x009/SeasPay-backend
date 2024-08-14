from dataclasses import dataclass

from src.domain.common import ValueObject


@dataclass(frozen=True)
class UserID(ValueObject[int]):
    value: int
    