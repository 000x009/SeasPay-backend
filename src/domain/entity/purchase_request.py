from typing import Optional
from datetime import datetime, UTC

from src.domain.value_objects.purchase_request import (
    PurchaseURL,
    PurchaseRequestId,
    CreatedAt,
    PurchaseRequestStatus,
    MessageID,
)
from src.domain.value_objects.user import UserID


class PurchaseRequest:
    __slots__ = (
        'id',
        'user_id',
        'purchase_url',
        'created_at',
        'status',
        'message_id',
    )

    def __init__(
        self,
        id: PurchaseRequestId,
        user_id: UserID,
        purchase_url: PurchaseURL,
        created_at: Optional[CreatedAt] = None,
        status: Optional[PurchaseRequestStatus] = None,
        message_id: Optional[MessageID] = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.purchase_url = purchase_url
        self.created_at = created_at
        self.status = status
        self.message_id = message_id

        if not self.created_at:
            self.created_at = CreatedAt(datetime.now(UTC))
