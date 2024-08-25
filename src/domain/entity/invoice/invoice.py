from __future__ import annotations
from datetime import datetime, UTC
from typing import Optional, Union, Any

from src.domain.value_objects.invoice import InvoiceStatus
from src.domain.value_objects.order import OrderID
from src.domain.value_objects.invoice import InvoiceID, CreatedAt


class Invoice:
    __slots__ = (
        'invoice_id',
        'order_id',
        'status',
        'created_at',
    )

    def __init__(
        self,
        invoice_id: InvoiceID,
        order_id: OrderID,
        status: InvoiceStatus,
        created_at: Optional[CreatedAt] = None,
    ):
        self.invoice_id = invoice_id
        self.order_id = order_id
        self.status = status
        self.created_at = created_at

        if not self.created_at:
            self.created_at = datetime.now(UTC)

    def __eq__(self, other: Union[Invoice, Any]) -> bool:
        if isinstance(other, Invoice) and other.invoice_id == self.invoice_id:
            return True
        return False

    def update_status(self, new_status: InvoiceStatus) -> None:
        self.status.value = new_status
