from decimal import Decimal
from typing import Optional
from datetime import datetime, UTC

from src.domain.value_objects.completed_order import (
    PaypalReceivedAmount,
    UserReceivedAmount,
    CompletedAt,
)
from src.domain.value_objects.order import OrderID, CreatedAt


class CompletedOrder:
    __slots__ = (
        'order_id',
        'paypal_received_amount',
        'user_received_amount',
        'completed_at',
    )

    def __init__(
        self,
        order_id: OrderID,
        paypal_received_amount: Optional[PaypalReceivedAmount] = None,
        user_received_amount: Optional[UserReceivedAmount] = None,
        completed_at: Optional[CompletedAt] = None,
    ):
        self.order_id = order_id
        self.paypal_received_amount = paypal_received_amount
        self.user_received_amount = user_received_amount
        self.completed_at = completed_at

        if not self.completed_at:
            self.completed_at = CompletedAt(datetime.now(UTC))

    def get_taken_summa(self) -> Decimal:
        return self.paypal_received_amount.value - self.user_received_amount.value

    def get_withdrawal_timespan(self, order_created_at: CreatedAt) -> int:
        difference = self.completed_at.value - order_created_at.value

        return difference.days

    def __str__(self) -> str:
        return f'<CompletedOrder: {self.order_id}>'

    def __repr__(self) -> str:
        return self.__str__()
