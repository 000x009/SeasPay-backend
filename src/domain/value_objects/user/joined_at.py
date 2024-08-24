from datetime import datetime, date

from src.domain.common.value_objects import ValueObject


class UserJoinedAt(ValueObject[datetime]):
    value: datetime

    def read(self) -> date:
        return self.value.date()
    