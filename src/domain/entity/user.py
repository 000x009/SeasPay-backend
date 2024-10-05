from __future__ import annotations
from typing import Union, Any

from src.domain.value_objects.user import UserID, JoinedAt, TotalWithdrawn, Commission
from src.domain.value_objects.completed_order import PaypalReceivedAmount
from src.domain.value_objects.order import MustReceiveAmount
from src.infrastructure.config import load_settings


class User:
    __slots__ = (
        'user_id',
        'joined_at',
        'commission',
        'total_withdrawn',
    )

    def __init__(
        self,
        user_id: UserID,
        joined_at: JoinedAt,
        commission: Commission,
        total_withdrawn: TotalWithdrawn,
    ) -> None:
        self.user_id = user_id
        self.joined_at = joined_at
        self.commission = commission
        self.total_withdrawn = total_withdrawn

    def __str__(self):
        return f'User <{self.user_id}>'

    def __eq__(self, other: Union[User, Any]) -> bool:
        if isinstance(other, User) and other.user_id == self.user_id:
            return True
        return False

    def update_commission(self, paypal_received_amount: PaypalReceivedAmount) -> MustReceiveAmount:
        total_withdrawn = TotalWithdrawn(self.total_withdrawn.value + paypal_received_amount.value)

        if self.commission.value == load_settings().commission.paypal.min_percentage_to_withdraw:
            return
        elif total_withdrawn.value >= 10 and total_withdrawn.value < 20:
            self.commission = Commission(13)
        elif total_withdrawn.value >= 20 and total_withdrawn.value < 50:
            self.commission = Commission(10)
        elif total_withdrawn.value >= 100 and total_withdrawn.value < 200:
            self.commission = Commission(7)

        commission_percentage = self.commission.value / 100
        user_amount = paypal_received_amount.value * commission_percentage
        return MustReceiveAmount(user_amount)
    