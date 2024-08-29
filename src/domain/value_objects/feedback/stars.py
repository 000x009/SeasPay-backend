from dataclasses import dataclass

from src.domain.common import ValueObject
from src.domain.exceptions.feedback import InvalidFeedbackStarsError


@dataclass(frozen=True)
class Stars(ValueObject[int]):
    value: int

    def _validate(self) -> None:
        if self.value < 0 or self.value > 5:
            raise InvalidFeedbackStarsError('Stars amount must be greater than 0 and less than 5.')
