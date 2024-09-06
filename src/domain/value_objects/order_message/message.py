from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.order_message import LongMessageError


@dataclass(frozen=True)
class Message(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) > 4096:
            raise LongMessageError(f"Message is too long: {len(self.value)} > 4096")
