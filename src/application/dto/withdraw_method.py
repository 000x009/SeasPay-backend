from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from src.domain.value_objects.withdraw_method import MethodEnum


@dataclass(frozen=True)
class WithdrawMethodDTO:
    id: int
    order_id: UUID
    method: MethodEnum
    card_number: Optional[str] = field(default=None)
    card_holder_name: Optional[str] = field(default=None)
    crypto_address: Optional[str] = field(default=None)
    crypto_network: Optional[str] = field(default=None)


@dataclass(frozen=True)
class AddWithdrawMethodDTO:
    order_id: UUID
    method: MethodEnum
    card_number: Optional[str] = field(default=None)
    card_holder_name: Optional[str] = field(default=None)
    crypto_address: Optional[str] = field(default=None)
    crypto_network: Optional[str] = field(default=None)


@dataclass(frozen=True)
class GetWithdrawMethodDTO:
    order_id: UUID
