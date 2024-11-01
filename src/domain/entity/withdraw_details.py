from typing import Optional
from decimal import Decimal

from src.domain.value_objects.order import OrderID, MustReceiveAmount
from src.domain.value_objects.withdraw_method import (
    Method,
    CardHolderName,
    CardNumber,
    CryptoAddress,
    CryptoNetwork,
    MethodEnum,
    PaymentReceipt,
    WithdrawCommission,
)
from src.domain.exceptions.withdraw_details import (
    CardNumberError,
    CardHolderNameError,
    CryptoAddressError,
    CryptoNetworkError,
)
from src.domain.value_objects.user import TotalWithdrawn
from src.domain.value_objects.completed_order import PaymentSystemReceivedAmount
from src.infrastructure.config import app_settings


class WithdrawDetails:
    __slots__ = (
        'order_id',
        'method',
        'card_number',
        'card_holder_name',
        'crypto_address',
        'crypto_network',
        'payment_receipt',
        'commission',
    )

    def __init__(
        self,
        order_id: OrderID,
        method: Method,
        card_number: Optional[CardNumber] = None,
        card_holder_name: Optional[CardHolderName] = None,
        crypto_address: Optional[CryptoAddress] = None,
        crypto_network: Optional[CryptoNetwork] = None,
        payment_receipt: Optional[PaymentReceipt] = None,
        commission: Optional[WithdrawCommission] = None,
    ) -> None:
        self.order_id = order_id
        self.method = method
        self.card_number = card_number
        self.card_holder_name = card_holder_name
        self.crypto_address = crypto_address
        self.crypto_network = crypto_network
        self.payment_receipt = payment_receipt
        self.commission = commission

    def __post_init__(self) -> None:
        if self.method.value == MethodEnum.CARD:
            if self.card_number is None:
                raise CardNumberError('Card number is required for card method')
            if self.card_holder_name is None:
                raise CardHolderNameError('Card holder name is required for card method')
        elif self.method.value == MethodEnum.CRYPTO:
            if self.crypto_address is None:
                raise CryptoAddressError('Crypto address is required for crypto method')
            if self.crypto_network is None:
                raise CryptoNetworkError('Crypto network is required for crypto method')

    def set_commission(
        self,
        payment_system_received_amount: PaymentSystemReceivedAmount,
        user_total_withdrawn: TotalWithdrawn,
    ) -> Optional[WithdrawCommission]:
        total_withdrawn = TotalWithdrawn(user_total_withdrawn.value + payment_system_received_amount.value)
        min_commission = app_settings.commission.min_withdraw_percentage
        commission = self.commission.value

        if total_withdrawn.value > 500:
            commission = min_commission
        elif total_withdrawn.value > 300:
            commission = 8
        elif total_withdrawn.value > 200:
            commission = 9
        elif total_withdrawn.value > 150:
            commission = 10
        elif total_withdrawn.value > 100:
            commission = 11
        elif total_withdrawn.value > 70:
            commission = 12
        elif total_withdrawn.value > 50:
            commission = 13
        elif total_withdrawn.value > 30:
            commission = 14

        self.commission = WithdrawCommission(Decimal(commission))
        return self.commission

    def calculate_amount_user_must_receive(
        self,
        payment_system_received_amount: PaymentSystemReceivedAmount,
    ) -> MustReceiveAmount:
        commission_percentage = Decimal(self.commission.value / 100)
        commission_amount = payment_system_received_amount.value * commission_percentage
        user_amount = payment_system_received_amount.value - commission_amount

        return MustReceiveAmount(round(user_amount, 2))
