from __future__ import annotations
from datetime import datetime, UTC
from typing import Union, Any, Optional

from src.domain.value_objects.user import UserID
from src.domain.value_objects.order import PaymentReceipt, CreatedAt, OrderStatus, OrderID


class Order:
    __slots__ = (
        'id',
        'user_id',
        'payment_receipt',
        'created_at',
        'status',
    )

    def __init__(
        self,
        user_id: UserID,
        payment_receipt: PaymentReceipt,
        id: Optional[OrderID] = None,
        created_at: Optional[CreatedAt] = None,
        status: Optional[OrderStatus] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.payment_receipt = payment_receipt
        self.created_at = created_at
        self.status = status

        if not created_at:
            self.created_at = CreatedAt(datetime.now(UTC))
        if not status:
            self.status = OrderStatus.WAIT

    def __str__(self):
        return f'Order <{self.invoice_id}>'

    def __eq__(self, other: Union[Order, Any]) -> bool:
        if isinstance(other, Order) and other.invoice_id == self.invoice_id:
            return True
        return False
