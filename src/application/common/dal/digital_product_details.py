from typing import Protocol
from abc import abstractmethod

from src.domain.entity.digital_product_details import DigitalProductDetails
from src.domain.value_objects.order import OrderID


class BaseTransferDetailsDAL(Protocol):
    @abstractmethod
    async def insert(self, withdraw_method: DigitalProductDetails) -> DigitalProductDetails:
        raise NotImplementedError

    @abstractmethod
    async def get(self, order_id: OrderID) -> DigitalProductDetails:
        raise NotImplementedError
