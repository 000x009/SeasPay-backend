from dataclasses import dataclass

from src.domain.common import ValueObject


@dataclass(frozen=True)
class FeedbackID(ValueObject[int]):
    value: int
