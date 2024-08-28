from __future__ import annotations

from datetime import datetime, UTC
from typing import Union, Any, Optional

from src.domain.value_objects.user import UserID
from src.domain.value_objects.invoice import InvoiceID
from src.domain.value_objects.order import PaymentReceipt, FinalAmount, CreatedAt, OrderStatus, OrderID


class Order:
    __slots__ = (
        'id',
        'user_id',
        'invoice_id',
        'payment_receipt',
        'final_amount',
        'created_at',
        'status',
    )

    def __init__(
        self,
        id: OrderID,
        user_id: UserID,
        invoice_id: InvoiceID,
        payment_receipt: PaymentReceipt,
        final_amount: FinalAmount,
        created_at: Optional[CreatedAt],
        status: Optional[OrderStatus]
    ):
        self.id = id
        self.user_id = user_id
        self.invoice_id = invoice_id
        self.payment_receipt = payment_receipt
        self.final_amount = final_amount
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
