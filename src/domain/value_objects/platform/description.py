from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.platform import InvalidDescriptionError


@dataclass(frozen=True)
class Description(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 500:
            raise InvalidDescriptionError('Description cannot be longer than 500 characters')
