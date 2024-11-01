from dataclasses import dataclass
from enum import StrEnum

from src.domain.common.value_objects import ValueObject


class OrderTypeEnum(StrEnum):
    WITHDRAW = "WITHDRAW"
    TRANSFER = "TRANSFER"
    DIGITAL_PRODUCT = "DIGITAL_PRODUCT"


@dataclass(frozen=True)
class OrderType(ValueObject[OrderTypeEnum]):
    value: OrderTypeEnum
