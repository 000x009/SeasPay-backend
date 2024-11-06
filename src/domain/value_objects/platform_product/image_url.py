import re
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.platform_product import InvalidImageURL


@dataclass(frozen=True)
class ImageURL(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if not re.match(r"^https?://", self.value):
            raise InvalidImageURL(f"Invalid image URL: {self.value}")
