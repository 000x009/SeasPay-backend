from typing import Protocol, List, Optional
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

    @abstractmethod
    async def get_total(self) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, platform_id: PlatformID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        platform_id: PlatformID,
        updated_platform: Platform,
    ) -> PlatformDB:
        raise NotImplementedError
