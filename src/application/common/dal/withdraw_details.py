from typing import Protocol
from abc import abstractmethod

from src.domain.entity.withdraw_details import WithdrawDetails
from src.domain.value_objects.order import OrderID


class BaseWithdrawDetailsDAL(Protocol):
    @abstractmethod
    async def insert(self, withdraw_method: WithdrawDetails) -> WithdrawDetails:
        raise NotImplementedError

    @abstractmethod
    async def get(self, order_id: OrderID) -> WithdrawDetails:
        raise NotImplementedError
