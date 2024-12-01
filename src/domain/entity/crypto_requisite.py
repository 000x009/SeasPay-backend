from typing import Optional

from src.domain.value_objects.requisite import RequisiteId, RequisiteType
from src.domain.value_objects.crypto_requisite import WalletAddress, Network, Asset, Memo


class CryptoRequisite:
    __slots__ = (
        "requisite_id",
        "type",
        "wallet_address",
        "network",
        "asset",
        "memo",
    )

    def __init__(
        self,
        requisite_id: RequisiteId,
        type: RequisiteType,
        wallet_address: WalletAddress,
        network: Network,
        asset: Asset,
        memo: Optional[Memo] = None,
    ) -> None:
        self.requisite_id = requisite_id
        self.type = type
        self.wallet_address = wallet_address
        self.network = network
        self.asset = asset
        self.memo = memo
