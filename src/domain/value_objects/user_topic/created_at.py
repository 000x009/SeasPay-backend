from dataclasses import dataclass
from datetime import datetime

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class CreatedAt(ValueObject[datetime]):
    value: datetime
    