from dataclasses import dataclass

from src.domain.common import ValueObject
from src.domain.exceptions.feedback import InvalidFeedbackCommentError


@dataclass(frozen=True)
class Comment(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 5000:
            raise InvalidFeedbackCommentError('Comment length must be less than 5000.')
