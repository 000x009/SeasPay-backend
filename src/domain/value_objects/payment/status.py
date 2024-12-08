from dataclasses import dataclass
from enum import Enum

from src.domain.common.value_objects import ValueObject


class PaymentStatusEnum(Enum):
    ACTIVE = "ACTIVE"
    PAID = "PAID"
    FAILED = "FAILED"


@dataclass(frozen=True)
class PaymentStatus(ValueObject[PaymentStatusEnum]):
    value: PaymentStatusEnum
