from typing import Protocol, List
from abc import abstractmethod

from src.domain.value_objects.platform import PlatformID
from src.domain.entity.platform_product import PlatformProduct, PlatformProductDB
from src.domain.value_objects.platform_product import PlatformProductID


class PlatformProductDAL(Protocol):
    @abstractmethod
    async def get(self, platform_id: PlatformProductID) -> PlatformProductDB:
        raise NotImplementedError

    @abstractmethod
    async def list_(self, platform_id: PlatformID, limit: int, offset: int) -> List[PlatformProductDB]:
        raise NotImplementedError

    @abstractmethod
    async def insert(self, platform: PlatformProduct) -> PlatformProductDB:
        raise NotImplementedError

    @abstractmethod
    async def get_total(self, platform_id: PlatformID) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, platform_id: PlatformProductID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, platform_product: PlatformProductDB) -> PlatformProductDB:
        raise NotImplementedError

