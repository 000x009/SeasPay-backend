from typing import Protocol
from abc import abstractmethod

from src.domain.entity.withdraw_method import WithdrawMethod
from src.domain.value_objects.order import OrderID


class BaseWithdrawMethodDAL(Protocol):
    @abstractmethod
    async def insert(self, withdraw_method: WithdrawMethod) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, order_id: OrderID) -> WithdrawMethod:
        raise NotImplementedError
