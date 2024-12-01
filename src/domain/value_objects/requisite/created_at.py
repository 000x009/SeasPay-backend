from datetime import datetime

from src.domain.common.value_objects import ValueObject

class CreatedAt(ValueObject[datetime]):
    value: datetime
