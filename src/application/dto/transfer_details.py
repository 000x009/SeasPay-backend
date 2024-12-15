from uuid import UUID
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class TransferDetailsDTO:
    order_id: UUID
    receiver_email: str
    amount: Decimal
    receipt_photo_url: str
    commission: Decimal


@dataclass(frozen=True)
class AddTransferDetailsDTO:
    order_id: UUID
    receiver_email: str
    amount: Decimal
    commission: Decimal
    receipt_photo_url: Optional[str] = field(default=None)


@dataclass(frozen=True)
class GetTransferDetailsDTO:
    order_id: UUID


@dataclass(frozen=True)
class CalculateTransferCommissionDTO:
    order_id: UUID
    payment_system_received_amount: Decimal


@dataclass(frozen=True)
class CalculationsDTO:
    transfer_commission: Decimal
    recipient_must_receive: Decimal
