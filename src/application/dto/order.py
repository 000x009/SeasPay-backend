from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional
from decimal import Decimal
from uuid import UUID

from src.domain.entity.order import OrderStatusEnum
from src.application.common.dto import Pagination, FileDTO
from src.application.dto.withdraw_method import WithdrawMethodDTO, AddWithdrawMethodDTO


@dataclass(frozen=True)
class OrderDTO:
    id: UUID
    user_id: int
    payment_receipt: str
    commission: int
    withdraw_method: WithdrawMethodDTO
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
class CreateOrderDTO:
    user_id: int
    payment_receipt: str
    withdraw_method: AddWithdrawMethodDTO
    receipt_photo: FileDTO = field(default=None)
    created_at: datetime = field(default=datetime.now(UTC))
    status: OrderStatusEnum = field(default=OrderStatusEnum.NEW)
    telegram_message_id: Optional[int] = field(default=None)


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
