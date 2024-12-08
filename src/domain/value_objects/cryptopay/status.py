from enum import Enum

from src.domain.common.value_objects import ValueObject


class InvoiceStatus(Enum):
    ACTIVE = "active"
    PAID = "paid"
    EXPIRED = "expired"


class InvoiceStatus(ValueObject[InvoiceStatus]):
    value: InvoiceStatus
