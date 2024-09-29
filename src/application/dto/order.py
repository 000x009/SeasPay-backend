from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional, Union

from src.domain.entity.order import OrderStatus
from src.application.common.dto import Pagination
from src.application.dto.withdraw_method import CardMethodDTO, CryptoMethodDTO


@dataclass(frozen=True)
class OrderDTO:
    id: int
    user_id: int
    payment_receipt: str
    withdraw_method: Union[CardMethodDTO, CryptoMethodDTO]
    created_at: Optional[datetime] = field(default=datetime.now(UTC))
    status: Optional[OrderStatus] = field(default=OrderStatus.NEW)
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
    withdraw_method: Union[CardMethodDTO, CryptoMethodDTO]
    created_at: datetime = field(default=datetime.now(UTC))
    status: OrderStatus = field(default=OrderStatus.NEW)
    telegram_message_id: Optional[int] = field(default=None)


@dataclass(frozen=True)
class TakeOrderDTO:
    order_id: int


@dataclass(frozen=True)
class AddTelegramMessageIdDTO:
    order_id: int
    telegram_message_id: int
    