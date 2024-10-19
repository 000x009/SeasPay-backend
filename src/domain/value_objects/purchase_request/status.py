from enum import StrEnum
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


class RequestStatusEnum(StrEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class PurchaseRequestStatus(ValueObject[RequestStatusEnum]):
    value: RequestStatusEnum
