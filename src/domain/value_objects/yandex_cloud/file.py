from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class File(ValueObject[bytes]):
    value: bytes
