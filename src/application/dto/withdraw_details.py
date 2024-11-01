from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID
from decimal import Decimal

from src.domain.value_objects.withdraw_method import MethodEnum


@dataclass(frozen=True)
class WithdrawDetailsDTO:
    order_id: UUID
    method: MethodEnum
    payment_receipt: str
    commission: Decimal
    card_number: Optional[str] = field(default=None)
    card_holder_name: Optional[str] = field(default=None)
    crypto_address: Optional[str] = field(default=None)
    crypto_network: Optional[str] = field(default=None)


@dataclass(frozen=True)
class AddWithdrawDetailsDTO:
    order_id: UUID
    method: MethodEnum
    payment_receipt: str
    commission: Decimal
    card_number: Optional[str] = field(default=None)
    card_holder_name: Optional[str] = field(default=None)
    crypto_address: Optional[str] = field(default=None)
    crypto_network: Optional[str] = field(default=None)


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
