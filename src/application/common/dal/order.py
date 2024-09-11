from typing import Protocol, List, Optional
from abc import abstractmethod

from src.domain.value_objects.user import UserID
from src.application.dto.order import OrderDTO
from src.domain.value_objects.order import OrderID
from src.domain.entity.order import Order


class BaseOrderDAL(Protocol):
    @abstractmethod
    async def list_(
        self, user_id: UserID, limit: int, offset: int
    ) -> Optional[List[OrderDTO]]:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self, user_id: UserID, order_id: OrderID,
    ) -> Optional[OrderDTO]:
        raise NotImplementedError

    @abstractmethod
    async def insert(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, order: Order) -> Optional[Order]:
        raise 
    