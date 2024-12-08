from typing import Optional
from datetime import datetime, UTC
from uuid import uuid4

from src.domain.value_objects.payment import (
    Amount,
    CreatedAt,
    InvoiceURL,
    PaymentStatus,
    PaymentID,
    PaymentStatusEnum,
)
from src.domain.value_objects.user import UserID


class Payment:
    __slots__ = (
        "id",
        "user_id",
        "invoice_url",
        "amount",
        "status",
        "created_at",
    )

    def __init__(
        self,
        user_id: UserID,
        amount: Amount,
        invoice_url: Optional[InvoiceURL] = None,
        status: Optional[PaymentStatus] = None,
        id: Optional[PaymentID] = None,
        created_at: Optional[CreatedAt] = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.invoice_url = invoice_url
        self.amount = amount
        self.status = status
        self.created_at = created_at

        if not created_at:
            self.created_at = CreatedAt(datetime.now(UTC))
        if not id:
            self.id = PaymentID(uuid4())
        if not status:
            self.status = PaymentStatus(PaymentStatusEnum.ACTIVE)
