from src.domain.value_objects.order import OrderID
from src.domain.value_objects.crypto_details import CryptoDetailsID, CryptoAddress, Network


class CryptoDetails:
    __slots__ = (
        'order_id',
        'crypto_address',
        'network',
    )

    def __init__(
        self,
        order_id: OrderID,
        crypto_address: CryptoAddress,
        network: Network,
    ) -> None:
        self.order_id = order_id
        self.crypto_address = crypto_address
        self.network = network


class CryptoDetailsDB(CryptoDetails):
    __slots__ = ("id",)

    def __init__(
        self,
        id: CryptoDetailsID,
        order_id: OrderID,
        crypto_address: CryptoAddress,
        network: Network,
    ) -> None:
        self.id = id
        self.order_id = order_id
        self.crypto_address = crypto_address
        self.network = network
