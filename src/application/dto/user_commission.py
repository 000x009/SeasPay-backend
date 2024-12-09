from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class UserCommissionDTO:
    user_id: int
    transfer: Decimal
    withdraw: Decimal
    digital_product: Decimal


@dataclass(frozen=True)
class CreateUserCommissionDTO:
    user_id: int
    transfer: Decimal
    withdraw: Decimal
    digital_product: Decimal


@dataclass(frozen=True)
class GetUserCommissionDTO:
    user_id: int


@dataclass(frozen=True)
class UpdateUserCommissionDTO:
    user_id: int
    transfer: Decimal
    withdraw: Decimal
    digital_product: Decimal


@dataclass(frozen=True)
class CalculateWithdrawCommissionDTO:
    order_id: UUID
    payment_system_received_amount: Decimal


@dataclass(frozen=True)
class CalculateTransferCommissionDTO:
    order_id: UUID
    payment_system_received_amount: Decimal


@dataclass(frozen=True)
class CountCommissionDTO:
    amount: Decimal
    user_id: int


@dataclass(frozen=True)
class CountCommissionResultDTO:
    withdraw_final_rub: Decimal
    transfer_final_rub: Decimal
    digital_product_final_rub: Decimal
    withdraw_final_usd: Decimal
    transfer_final_usd: Decimal
    digital_product_final_usd: Decimal

