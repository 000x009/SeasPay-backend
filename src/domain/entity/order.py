from __future__ import annotations

import uuid
from datetime import datetime, UTC
from typing import Union, Any, Optional
from decimal import Decimal

from src.domain.value_objects.user import UserID
from src.domain.value_objects.order import (
    PaymentReceipt,
    CreatedAt,
    OrderStatus,
    OrderID,
    OrderStatusEnum,
    Commission,
)
from src.domain.value_objects.order_message import MessageID
from src.domain.value_objects.completed_order import PaymentSystemReceivedAmount
from src.domain.value_objects.order import MustReceiveAmount, OrderType


class Order:
    __slots__ = (
        'id',
        'user_id',
        'type_',
        'payment_receipt',
        'created_at',
        'status',
        'message_id',
        'telegram_message_id',
    )

    def __init__(
        self,
        user_id: UserID,
        payment_receipt: PaymentReceipt,
        type_: OrderType,
        id: Optional[OrderID] = None,
        created_at: Optional[CreatedAt] = None,
        status: Optional[OrderStatus] = None,
        telegram_message_id: Optional[MessageID] = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.payment_receipt = payment_receipt
        self.created_at = created_at
        self.status = status
        self.telegram_message_id = telegram_message_id
        self.type_ = type_

        if not created_at:
            self.created_at = CreatedAt(datetime.now(UTC))
        if not status:
            self.status = OrderStatus(OrderStatusEnum.NEW)
        if not id:
            self.id = OrderID(uuid.uuid4())

    def __str__(self):
        return f'Order <{self.id}>'

    def __eq__(self, other: Union[Order, Any]) -> bool:
        if isinstance(other, Order) and other.id == self.id:
            return True
        return False

    def calculate_commission(
            self,
            commission: Commission,
            payment_system_received_amount: PaymentSystemReceivedAmount,
    ) -> MustReceiveAmount:
        commission_percentage = Decimal(commission.value / 100)
        commission_amount = payment_system_received_amount.value * commission_percentage
        user_amount = payment_system_received_amount.value - commission_amount

        return MustReceiveAmount(user_amount)
