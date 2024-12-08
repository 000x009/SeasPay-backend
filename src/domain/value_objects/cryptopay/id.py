from datetime import datetime

from src.domain.common.value_objects import ValueObject


class InvoiceID(ValueObject[int]):
    value: int
