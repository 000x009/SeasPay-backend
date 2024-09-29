from src.domain.value_objects.order import OrderID
from src.domain.value_objects.withdraw_method import Method, CardHolderName, CardNumber, CryptoAddress, Network
from src.domain.value_objects.common.db_identity import DBIdentity


class WithdrawMethod:
    __slots__ = ('id', 'order_id', 'method')

    def __init__(
        self,
        order_id: OrderID,
        method: Method,
    ) -> None:
        self.id = id
        self.order_id = order_id
        self.method = method


class CardMethod(WithdrawMethod):
    __slots__ = ('card_number', 'card_holder_name')

    def __init__(
        self,
        order_id: OrderID,
        method: Method,
        card_number: CardNumber,
        card_holder_name: CardHolderName,
    ) -> None:
        self.id = id
        self.order_id = order_id
        self.method = method
        self.card_number = card_number
        self.card_holder_name = card_holder_name


class CryptoMethod(WithdrawMethod):
    __slots__ = ('crypto_address', 'network')

    def __init__(
        self,
        order_id: OrderID,
        method: Method,
        crypto_address: CryptoAddress,
        network: Network,
    ) -> None:
        self.id = id
        self.order_id = order_id
        self.method = method
        self.crypto_address = crypto_address
        self.network = network


class DBCardMethod(WithdrawMethod):
    __slots__ = ('card_number', 'card_holder_name')

    def __init__(
        self,
        id: DBIdentity,
        order_id: OrderID,
        method: Method,
        card_number: CardNumber,
        card_holder_name: CardHolderName,
    ) -> None:
        self.id = id
        self.order_id = order_id
        self.method = method
        self.card_number = card_number
        self.card_holder_name = card_holder_name


class DBCryptoMethod(WithdrawMethod):
    __slots__ = ('crypto_address', 'network')

    def __init__(
        self,
        id: DBIdentity,
        order_id: OrderID,
        method: Method,
        crypto_address: CryptoAddress,
        network: Network,
    ) -> None:
        self.id = id
        self.order_id = order_id
        self.method = method
        self.crypto_address = crypto_address
        self.network = network
