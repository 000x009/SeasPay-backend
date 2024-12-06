from decimal import Decimal

from src.domain.value_objects.user import UserID
from src.domain.value_objects.user_commission import (
    UserWithdrawCommission,
    UserTransferCommission,
    UserDigitalProductCommission
)
from src.infrastructure.config import app_settings


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

    def update_withdraw_commission(self) -> UserWithdrawCommission:
        min_commission = app_settings.commission.min_withdraw_percentage
        commission = self.withdraw.value
        if commission > min_commission:
            commission = commission - 1
        self.withdraw = UserWithdrawCommission(Decimal(commission))

        return self.withdraw

    def update_transfer_commission(self) -> UserTransferCommission:
        min_commission = app_settings.commission.min_transfer_percentage
        commission = self.transfer.value
        if commission > min_commission:
            commission = commission - 1
        self.transfer = UserTransferCommission(Decimal(commission))

        return self.transfer
