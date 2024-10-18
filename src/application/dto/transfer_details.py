from uuid import UUID
from decimal import Decimal
from dataclasses import dataclass


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
    receipt_photo_url: str
    commission: Decimal


@dataclass(frozen=True)
class GetTransferDetailsDTO:
    order_id: UUID
