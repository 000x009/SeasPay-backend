from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.user import EmptyValueError


class Commission(ValueObject[int]):
    value: int

    def _validate(self) -> None:
        if not self.value:
            raise EmptyValueError('Commission value is empty.')
