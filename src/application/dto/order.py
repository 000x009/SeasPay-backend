from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional

from src.domain.entity.order import OrderStatusEnum
from src.application.common.dto import Pagination, FileDTO
from src.application.dto.withdraw_method import WithdrawMethodDTO, AddWithdrawMethodDTO


@dataclass(frozen=True)
class OrderDTO:
    id: int
    user_id: int
    payment_receipt: str
    withdraw_method: WithdrawMethodDTO
    created_at: Optional[datetime] = field(default=datetime.now(UTC))
    status: Optional[OrderStatusEnum] = field(default=OrderStatusEnum.NEW)
    telegram_message_id: Optional[int] = field(default=None)


@dataclass(frozen=True)
class ListOrderDTO:
    user_id: int
    pagination: Pagination


@dataclass(frozen=True)
class GetOrderDTO:
    order_id: int


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
    order_id: int


@dataclass(frozen=True)
class AddTelegramMessageIdDTO:
    order_id: int
    telegram_message_id: int
    