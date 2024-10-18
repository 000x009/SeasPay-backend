from typing import Protocol
from abc import abstractmethod

from src.domain.entity.transfer_details import TransferDetails
from src.domain.value_objects.order import OrderID


class BaseTransferDetailsDAL(Protocol):
    @abstractmethod
    async def insert(self, withdraw_method: TransferDetails) -> TransferDetails:
        raise NotImplementedError

    @abstractmethod
    async def get(self, order_id: OrderID) -> TransferDetails:
        raise NotImplementedError
