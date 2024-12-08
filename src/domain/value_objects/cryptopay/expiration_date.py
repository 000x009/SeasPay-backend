from datetime import datetime

from src.domain.common.value_objects import ValueObject


class ExpirationDate(ValueObject[datetime]):
    value: datetime
