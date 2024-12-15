from decimal import Decimal

from src.domain.value_objects.user import UserID
from src.domain.value_objects.user_commission import (
    UserWithdrawCommission,
    UserTransferCommission,
    UserDigitalProductCommission
)
from src.infrastructure.config import app_settings

CRYPTO_USDT_COMMISSION = 3


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

    def count_withdraw_commission(self, amount: Decimal) -> Decimal:
        commission_amount = amount / 100 * self.withdraw.value
        final_amount = round(amount + commission_amount, 1)

        return Decimal(final_amount)

    def count_transfer_commission(self, amount: Decimal) -> Decimal:
        commission_amount = amount / 100 * self.transfer.value
        final_amount = round(amount + commission_amount, 1)

        return Decimal(final_amount)
    
    def count_transfer_crypto_usdt(self, amount: Decimal) -> Decimal:
        commission_amount = amount / 100 * self.transfer.value
        final_amount = round(amount + commission_amount, 1)
        crypto_usdt_commission = final_amount / 100 * CRYPTO_USDT_COMMISSION
        final_amount = round(final_amount + crypto_usdt_commission, 1)

        return Decimal(final_amount)
    
    def count_digital_product_crypto_usdt(self, amount: Decimal) -> Decimal:
        commission_amount = amount / 100 * self.digital_product.value
        final_amount = round(amount + commission_amount, 1)
        crypto_usdt_commission = final_amount / 100 * CRYPTO_USDT_COMMISSION
        final_amount = round(final_amount + crypto_usdt_commission, 1)

        return Decimal(final_amount)

    def count_digital_product_commission(self, amount_usd: Decimal) -> Decimal:
        return Decimal(amount_usd)
