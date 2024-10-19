from uuid import UUID
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class PurchaseRequestId(ValueObject[UUID]):
    value: UUID
