from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.platform_product import InvalidImageURLError


@dataclass(frozen=True)
class Instruction(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 500:
            raise InvalidImageURLError('The instruction is too long. It must be less than 500 characters.')
