from decimal import Decimal
from typing import Optional
from datetime import datetime, UTC

from src.domain.value_objects.completed_order import (
    PaypalReceivedAmount,
    UserReceivedAmount,
    ReceivedAt,
    TakenCommission,
)
from src.domain.value_objects.order import OrderID, CreatedAt


class CompletedOrder:
    __slots__ = (
        'order_id',
        'paypal_received_amount',
        'user_received_amount',
        'received_at',
        'taken_commission',
    )

    def __init__(
        self,
        order_id: OrderID,
        paypal_received_amount: PaypalReceivedAmount,
        user_received_amount: UserReceivedAmount,
        taken_commission: TakenCommission,
        received_at: Optional[ReceivedAt] = None,
    ):
        self.order_id = order_id
        self.paypal_received_amount = paypal_received_amount
        self.user_received_amount = user_received_amount
        self.received_at = received_at
        self.taken_commission = taken_commission

        if not self.received_at:
            self.received_at = ReceivedAt(datetime.now(UTC))

    def get_taken_summa(self) -> Decimal:
        return self.paypal_received_amount.value - self.user_received_amount.value

    def get_withdrawal_timespan(self, order_created_at: CreatedAt) -> int:
        difference = self.received_at.value - order_created_at.value

        return difference.days

    def __str__(self) -> str:
        return f'<CompletedOrder: {self.order_id}>'

    def __repr__(self) -> str:
        return self.__str__()
