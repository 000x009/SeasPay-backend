from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.value_objects.payment import PaymentStatusEnum


@dataclass(frozen=True)
class PaymentDTO:
    id: UUID
    user_id: int
    invoice_url: str
    created_at: datetime
    status: PaymentStatusEnum
    amount: int


@dataclass(frozen=True)
class GetPaymentDTO:
    payment_id: UUID


@dataclass(frozen=True)
class CreatePaymentDTO:
    user_id: int
    amount: int


@dataclass(frozen=True)
class ReceivePaymentDTO:
    payment_id: UUID
