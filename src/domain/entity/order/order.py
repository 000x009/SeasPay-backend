from __future__ import annotations

from datetime import datetime, UTC
from typing import Union, Any, Optional

from src.domain.value_objects.user import UserID
from src.domain.value_objects.invoice import InvoiceID
from src.domain.value_objects.order import PaymentReceipt, FinalAmount, Time
from src.domain.entity.order import OrderStatus


class Order:
    __slots__ = (
        'user_id',
        'invoice_id',
        'payment_receipt',
        'final_amount',
        'time',
        'status'
    )

    def __init__(
        self,
        user_id: UserID,
        invoice_id: InvoiceID,
        payment_receipt: PaymentReceipt,
        final_amount: FinalAmount,
        time: Optional[Time],
        status: Optional[OrderStatus]
    ):
        self.user_id = user_id
        self.invoice_id = invoice_id
        self.payment_receipt = payment_receipt
        self.final_amount = final_amount
        self.time = time
        self.status = status

        if not time:
            self.time = Time(datetime.now(UTC))
        if not status:
            self.status = OrderStatus.WAIT

    def __str__(self):
        return f'Order <{self.invoice_id}>'

    def __eq__(self, other: Union[Order, Any]) -> bool:
        if isinstance(other, Order) and other.invoice_id == self.invoice_id:
            return True
        return False
