from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class PaymentReceipt(ValueObject[str]):
    value: str
