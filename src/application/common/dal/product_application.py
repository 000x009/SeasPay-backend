from typing import Protocol
from abc import abstractmethod

from src.domain.entity.product_application import ProductApplication
from src.domain.value_objects.product_application import ProductApplicationID


class ProductApplicationDAL(Protocol):
    @abstractmethod
    async def create(self, product_application: ProductApplication) -> ProductApplication:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, id: ProductApplicationID) -> ProductApplication:
        raise NotImplementedError

    @abstractmethod
    async def update(self, product_application: ProductApplication) -> ProductApplication:
        raise NotImplementedError
