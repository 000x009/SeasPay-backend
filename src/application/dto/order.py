from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional
from decimal import Decimal
from uuid import UUID

from src.domain.entity.order import OrderStatusEnum
from src.domain.value_objects.order import OrderType
from src.application.common.dto import Pagination
from src.application.dto.withdraw_details import AddWithdrawDetailsDTO
from src.domain.value_objects.withdraw_method import MethodEnum


@dataclass(frozen=True)
class OrderDTO:
    id: UUID
    user_id: int
    payment_receipt: str
    type: OrderType
    created_at: Optional[datetime] = field(default=datetime.now(UTC))
    status: Optional[OrderStatusEnum] = field(default=OrderStatusEnum.NEW)
    telegram_message_id: Optional[int] = field(default=None)


@dataclass(frozen=True)
class ListOrderDTO:
    user_id: int
    pagination: Optional[Pagination] = field(default=None)


@dataclass(frozen=True)
class GetOrderDTO:
    order_id: UUID


@dataclass(frozen=True)
class CreateWithdrawOrderDTO:
    user_id: int
    username: str
    payment_receipt_url: str
    method: MethodEnum
    created_at: datetime = field(default=datetime.now(UTC))
    status: OrderStatusEnum = field(default=OrderStatusEnum.NEW)
    telegram_message_id: Optional[int] = field(default=None)
    card_number: Optional[str] = field(default=None)
    card_holder_name: Optional[str] = field(default=None)
    crypto_address: Optional[str] = field(default=None)
    crypto_network: Optional[str] = field(default=None)



@dataclass(frozen=True)
class CreateTransferOrderDTO:
    user_id: int
    receiver_email: str
    username: str
    transfer_amount: Decimal
    payment_receipt_url: str


@dataclass(frozen=True)
class TakeOrderDTO:
    order_id: UUID


@dataclass(frozen=True)
class AddTelegramMessageIdDTO:
    order_id: UUID
    telegram_message_id: int


@dataclass(frozen=True)
class CalculateCommissionDTO:
    order_id: UUID
    paypal_received_amount: Decimal


@dataclass(frozen=True)
class CommissionDTO:
    commission: int
    user_must_receive: Decimal


@dataclass(frozen=True)
class FulfillOrderDTO:
    order_id: UUID
    paypal_received_amount: Decimal
    user_received_amount: Decimal


@dataclass(frozen=True)
class CancelOrderDTO:
    order_id: UUID
