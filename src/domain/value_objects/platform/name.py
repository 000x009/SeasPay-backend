from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.platform import InvalidPlatformNameError


@dataclass(frozen=True)
class Name(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 25:
            raise InvalidPlatformNameError('Name cannot be longer than 25 characters')
