from enum import StrEnum
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


class OrderStatusEnum(StrEnum):
    NOT_PAID = "NOT_PAID"
    COMPLETE = "COMPLETE"
    CANCEL = "CANCEL"
    PROCESSING = "PROCESSING"
    NEW = "NEW"
    DELAY = "DELAY"


@dataclass(frozen=True)
class OrderStatus(ValueObject[OrderStatusEnum]):
    value: OrderStatusEnum
