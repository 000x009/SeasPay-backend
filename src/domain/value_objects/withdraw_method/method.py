from enum import StrEnum
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


class MethodEnum(StrEnum):
    CARD = 'card'
    CRYPTO = 'crypto'


@dataclass(frozen=True)
class Method(ValueObject[MethodEnum]):
    value: MethodEnum
