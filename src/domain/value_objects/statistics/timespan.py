from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class TimeSpan(ValueObject[float]):
    """Timespan indicates in days"""

    value: float
