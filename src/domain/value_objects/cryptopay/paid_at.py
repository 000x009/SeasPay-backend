from datetime import datetime

from src.domain.common.value_objects import ValueObject


class PaidAt(ValueObject[datetime]):
    value: datetime
