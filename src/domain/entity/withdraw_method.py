from typing import Optional

from src.domain.value_objects.order import OrderID
from src.domain.value_objects.withdraw_method import (
    Method,
    CardHolderName,
    CardNumber,
    CryptoAddress,
    CryptoNetwork,
    MethodEnum,
    WithdrawMethodID,
)
from src.domain.exceptions.withdraw_method import (
    CardNumberError,
    CardHolderNameError,
    CryptoAddressError,
    CryptoNetworkError,
)


class WithdrawMethod:
    __slots__ = (
        'order_id',
        'method',
        'card_number',
        'card_holder_name',
        'crypto_address',
        'crypto_network',
    )

    def __init__(
        self,
        order_id: OrderID,
        method: Method,
        card_number: Optional[CardNumber] = None,
        card_holder_name: Optional[CardHolderName] = None,
        crypto_address: Optional[CryptoAddress] = None,
        crypto_network: Optional[CryptoNetwork] = None,
    ) -> None:
        self.order_id = order_id
        self.method = method
        self.card_number = card_number
        self.card_holder_name = card_holder_name
        self.crypto_address = crypto_address
        self.crypto_network = crypto_network

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


class DBWithdrawMethod(WithdrawMethod):
    __slots__ = (
        'id',
    )

    def __init__(
        self,
        id: WithdrawMethodID,
        order_id: OrderID,
        method: Method,
        card_number: Optional[CardNumber] = None,
        card_holder_name: Optional[CardHolderName] = None,
        crypto_address: Optional[CryptoAddress] = None,
        crypto_network: Optional[CryptoNetwork] = None,
    ) -> None:
        super().__init__(order_id, method, card_number, card_holder_name, crypto_address, crypto_network)
        self.id = id
