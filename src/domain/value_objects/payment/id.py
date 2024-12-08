from uuid import UUID
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class PaymentID(ValueObject[UUID]):
    value: UUID
