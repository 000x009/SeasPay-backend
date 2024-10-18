from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from src.domain.value_objects.withdraw_method import MethodEnum


@dataclass(frozen=True)
class WithdrawDetailsDTO:
    order_id: UUID
    method: MethodEnum
    payment_receipt: str
    commission: int
    card_number: Optional[str] = field(default=None)
    card_holder_name: Optional[str] = field(default=None)
    crypto_address: Optional[str] = field(default=None)
    crypto_network: Optional[str] = field(default=None)


@dataclass(frozen=True)
class AddWithdrawDetailsDTO:
    order_id: UUID
    method: MethodEnum
    payment_receipt: str
    commission: int
    card_number: Optional[str] = field(default=None)
    card_holder_name: Optional[str] = field(default=None)
    crypto_address: Optional[str] = field(default=None)
    crypto_network: Optional[str] = field(default=None)


@dataclass(frozen=True)
class GetWithdrawDetailsDTO:
    order_id: UUID
