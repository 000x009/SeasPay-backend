from __future__ import annotations
from typing import Union, Any

from src.domain.value_objects.user import (
    UserID,
    JoinedAt,
    TotalWithdrawn,
)
from src.domain.value_objects.completed_order import PaypalReceivedAmount
from src.infrastructure.config import load_settings
from src.domain.value_objects.transfer_details import Commission as TransferCommission
# from src.domain.value_objects.digital_product_details import Commission as ProductCommission
from src.domain.value_objects.withdraw_method import WithdrawCommission


class User:
    __slots__ = (
        'user_id',
        'joined_at',
        'withdraw_commission',
        'transfer_commission',
        'product_commission',
        'total_withdrawn',
    )

    def __init__(
        self,
        user_id: UserID,
        joined_at: JoinedAt,
        withdraw_commission: WithdrawCommission,
        transfer_commission: TransferCommission,
        product_commission: ProductCommission,
        total_withdrawn: TotalWithdrawn,
    ) -> None:
        self.user_id = user_id
        self.joined_at = joined_at
        self.withdraw_commission = withdraw_commission
        self.transfer_commission = transfer_commission
        self.product_commission = product_commission
        self.total_withdrawn = total_withdrawn

    def __str__(self):
        return f'User <{self.user_id}>'

    def __eq__(self, other: Union[User, Any]) -> bool:
        if isinstance(other, User) and other.user_id == self.user_id:
            return True
        return False

    def update_withdraw_commission(self, paypal_received_amount: PaypalReceivedAmount) -> None:
        total_withdrawn = TotalWithdrawn(self.total_withdrawn.value + paypal_received_amount.value)

        if self.withdraw_commission.value == load_settings().commission.paypal.min_percentage_to_withdraw:
            return
        elif total_withdrawn.value >= 10 and total_withdrawn.value < 20:
            self.withdraw_commission = WithdrawCommission(13)
        elif total_withdrawn.value >= 20 and total_withdrawn.value < 50:
            self.withdraw_commission = WithdrawCommission(10)
        elif total_withdrawn.value >= 100 and total_withdrawn.value < 200:
            self.withdraw_commission = WithdrawCommission(7)
