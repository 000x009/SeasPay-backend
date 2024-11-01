from decimal import Decimal

from src.domain.value_objects.user import UserID
from src.domain.value_objects.user_commission import (
    UserWithdrawCommission,
    UserTransferCommission,
    UserDigitalProductCommission
)
from src.infrastructure.config import app_settings
from src.domain.value_objects.user import TotalWithdrawn


class UserCommission:
    __slots__ = (
        'user_id',
        'transfer',
        'withdraw',
        'digital_product',
    )

    def __init__(
        self,
        user_id: UserID,
        transfer: UserTransferCommission,
        withdraw: UserWithdrawCommission,
        digital_product: UserDigitalProductCommission,
    ) -> None:
        self.user_id = user_id
        self.transfer = transfer
        self.withdraw = withdraw
        self.digital_product = digital_product

    def update_withdraw_commission(self, user_total_withdrawn: TotalWithdrawn) -> UserWithdrawCommission:
        min_commission = app_settings.commission.min_withdraw_percentage
        commission = self.withdraw.value

        if user_total_withdrawn.value > 500:
            commission = min_commission
        elif user_total_withdrawn.value > 300:
            commission = 8
        elif user_total_withdrawn.value > 200:
            commission = 9
        elif user_total_withdrawn.value > 150:
            commission = 10
        elif user_total_withdrawn.value > 100:
            commission = 11
        elif user_total_withdrawn.value > 70:
            commission = 12
        elif user_total_withdrawn.value > 50:
            commission = 13
        elif user_total_withdrawn.value > 30:
            commission = 14

        self.withdraw = UserWithdrawCommission(Decimal(commission))
        return self.withdraw

    def update_transfer_commission(self, user_total_withdrawn: TotalWithdrawn) -> UserTransferCommission:
        min_commission = app_settings.commission.min_transfer_percentage
        commission = self.withdraw.value

        if user_total_withdrawn.value > 500:
            commission = min_commission
        elif user_total_withdrawn.value > 300:
            commission = 8
        elif user_total_withdrawn.value > 200:
            commission = 9
        elif user_total_withdrawn.value > 150:
            commission = 10
        elif user_total_withdrawn.value > 100:
            commission = 11
        elif user_total_withdrawn.value > 70:
            commission = 12
        elif user_total_withdrawn.value > 50:
            commission = 13
        elif user_total_withdrawn.value > 30:
            commission = 14

        self.transfer = UserTransferCommission(Decimal(commission))
        return self.transfer
