from __future__ import annotations

import datetime
from typing import Union, Any, Optional

from src.domain.value_objects.user import (
    UserID,
    JoinedAt,
    TotalWithdrawn,
)


class User:
    __slots__ = (
        'user_id',
        'joined_at',
        'total_withdrawn',
    )

    def __init__(
        self,
        user_id: UserID,
        joined_at: Optional[JoinedAt] = None,
        total_withdrawn: Optional[TotalWithdrawn] = None,
    ) -> None:
        self.user_id = user_id
        self.joined_at = joined_at
        self.total_withdrawn = total_withdrawn

        if not self.total_withdrawn:
            self.total_withdrawn = TotalWithdrawn(0)
        if not self.joined_at:
            self.joined_at = JoinedAt(datetime.datetime.now(datetime.UTC))

    def __str__(self):
        return f'User <{self.user_id}>'

    def __eq__(self, other: Union[User, Any]) -> bool:
        if isinstance(other, User) and other.user_id == self.user_id:
            return True
        return False

    # def update_withdraw_commission(self, paypal_received_amount: PaypalReceivedAmount) -> None:
    #     total_withdrawn = TotalWithdrawn(self.total_withdrawn.value + paypal_received_amount.value)
    #
    #     if self.withdraw_commission.value == load_settings().commission.paypal.min_percentage_to_withdraw:
    #         return
    #     elif total_withdrawn.value >= 10 and total_withdrawn.value < 20:
    #         self.withdraw_commission = WithdrawCommission(13)
    #     elif total_withdrawn.value >= 20 and total_withdrawn.value < 50:
    #         self.withdraw_commission = WithdrawCommission(10)
    #     elif total_withdrawn.value >= 100 and total_withdrawn.value < 200:
    #         self.withdraw_commission = WithdrawCommission(7)
