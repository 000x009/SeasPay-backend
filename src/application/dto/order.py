from dataclasses import dataclass, field
from datetime import datetime, UTC

from src.domain.entity.order import OrderStatus
from src.application.common.dto import Pagination


@dataclass(frozen=True)
class OrderDTO:
    id: int
    user_id: int
    payment_receipt: str
    created_at: datetime = field(default=datetime.now(UTC))
    status: OrderStatus = field(default=OrderStatus.WAIT)


@dataclass(frozen=True)
class ListOrderDTO:
    user_id: int
    pagination: Pagination


@dataclass(frozen=True)
class GetOrderDTO:
    user_id: int
    order_id: int


@dataclass(frozen=True)
class CreateOrderDTO:
    user_id: int
    payment_receipt: str
    created_at: datetime = field(default=datetime.now(UTC))
    status: OrderStatus = field(default=OrderStatus.WAIT)
