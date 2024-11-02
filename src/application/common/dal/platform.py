from typing import Protocol, List
from abc import abstractmethod

from src.domain.value_objects.platform import PlatformID
from src.domain.entity.platform import PlatformDB, Platform


class PlatformDAL(Protocol):
    @abstractmethod
    async def get(self, platform_id: PlatformID) -> PlatformDB:
        raise NotImplementedError

    @abstractmethod
    async def list_(self, limit: int, offset: int) -> List[PlatformDB]:
        raise NotImplementedError

    @abstractmethod
    async def insert(self, platform: Platform) -> PlatformDB:
        raise NotImplementedError
