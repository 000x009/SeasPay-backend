from dataclasses import dataclass
from enum import StrEnum, auto

from src.domain.common.value_objects import ValueObject


class OrderTypeEnum(StrEnum):
    WITHDRAW = auto()
    TRANSFER = auto()
    DIGITAL_PRODUCT = auto()


@dataclass(frozen=True)
class OrderType(ValueObject[OrderTypeEnum]):
    value: OrderTypeEnum
