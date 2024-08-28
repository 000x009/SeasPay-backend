from typing import Protocol
from abc import abstractmethod

from src.domain.entity.completed_order import CompletedOrder
from src.domain.value_objects.completed_order import CompletedOrderID


class BaseCompletedOrderDAL(Protocol):
    @abstractmethod
    async def insert(self, completed_order: CompletedOrder) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, completed_order_id: CompletedOrderID) -> CompletedOrder:
        raise NotImplementedError
