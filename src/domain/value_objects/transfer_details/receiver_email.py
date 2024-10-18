import re
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.transfer_details import ReceiverEmailError


@dataclass(frozen=True)
class ReceiverEmail(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.value):
            raise ReceiverEmailError('Email address is invalid')
