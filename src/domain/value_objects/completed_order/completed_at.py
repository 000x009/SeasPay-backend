from dataclasses import dataclass
from datetime import datetime

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class CompletedAt(ValueObject[datetime]):
    value: datetime
