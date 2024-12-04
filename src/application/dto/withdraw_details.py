from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal


@dataclass(frozen=True)
class WithdrawDetailsDTO:
    order_id: UUID
    requisite_id: UUID
    payment_receipt: str
    commission: Decimal


@dataclass(frozen=True)
class AddWithdrawDetailsDTO:
    order_id: UUID
    requisite_id: UUID
    payment_receipt: str
    commission: Decimal


@dataclass(frozen=True)
class GetWithdrawDetailsDTO:
    order_id: UUID


@dataclass(frozen=True)
class CalculateWithdrawCommissionDTO:
    order_id: UUID
    payment_system_received_amount: Decimal


@dataclass(frozen=True)
class WithdrawCalculationsDTO:
    withdraw_commission: Decimal
    recipient_must_receive: Decimal
