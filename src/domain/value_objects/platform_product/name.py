from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.platform_product import InvalidProductNameError


@dataclass(frozen=True)
class ProductName(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 50:
            raise InvalidProductNameError('Product name must be less than 50 characters')
