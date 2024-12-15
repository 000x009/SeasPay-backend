from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional, Dict, List
from decimal import Decimal
from uuid import UUID

from src.domain.entity.order import OrderStatusEnum
from src.domain.value_objects.order import OrderTypeEnum


@dataclass(frozen=True)
class OrderDTO:
    id: UUID
    user_id: int
    type: OrderTypeEnum
    payment_receipt: Optional[str] = field(default=None)
    payment_id: Optional[UUID] = field(default=None)
    created_at: Optional[datetime] = field(default=datetime.now(UTC))
    status: Optional[OrderStatusEnum] = field(default=OrderStatusEnum.NEW)
    telegram_message_id: Optional[int] = field(default=None)


@dataclass(frozen=True)
class ListOrderDTO:
    user_id: int
    page: int = field(default=None)


@dataclass(frozen=True)
class GetOrderDTO:
    order_id: UUID


@dataclass(frozen=True)
class CreateWithdrawOrderDTO:
    user_id: int
    requisite_id: UUID
    username: str
    payment_receipt_url: str


@dataclass(frozen=True)
class CreateTransferOrderDTO:
    user_id: int
    receiver_email: str
    username: str
    transfer_amount: Decimal
    payment_receipt_url: Optional[str] = field(default=None)
    payment_id: Optional[UUID] = field(default=None)
    created_at: datetime = field(default=datetime.now(UTC))


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
    payment_system_received_amount: Decimal


@dataclass(frozen=True)
class CommissionDTO:
    commission: int
    user_must_receive: Decimal


@dataclass(frozen=True)
class FulfillWithdrawOrderDTO:
    order_id: UUID
    payment_system_received_amount: Optional[Decimal] = field(default=None)
    user_received_amount: Optional[Decimal] = field(default=None)


@dataclass(frozen=True)
class FulfillTransferOrderDTO:
    order_id: UUID


@dataclass(frozen=True)
class CancelOrderDTO:
    order_id: UUID


@dataclass(frozen=True)
class CreateDigitalProductOrderDTO:
    application_id: UUID
    user_id: int
    login_data: Dict[str, str]
    username: str
    payment_receipt_url: Optional[str] = field(default=None)
    payment_id: Optional[UUID] = field(default=None)


@dataclass(frozen=True)
class PurchasePlatformProductDTO:
    platform_product_id: int
    user_id: int
    login_data: Dict[str, str]
    username: str
    payment_receipt_url: Optional[str] = field(default=None)
    payment_id: Optional[UUID] = field(default=None)


@dataclass(frozen=True)
class FulfillDigitalProductOrderDTO:
    order_id: UUID


@dataclass(frozen=True)
class OrderListResultDTO:
    orders: List[OrderDTO]
    total: int


@dataclass(frozen=True)
class PayOrderDTO:
    payment_id: UUID
