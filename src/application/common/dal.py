from abc import abstractmethod, ABC
from typing import Protocol, Optional, List, TypeVar, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.common import ValueObject

T = TypeVar('T')


class DAL(Protocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @abstractmethod
    async def insert(self, values: T) -> None:
        pass
    
    @abstractmethod  
    async def get_one(self, values: T) -> Optional[T]:
        pass
    
    @abstractmethod
    async def get_all(self, values: T) -> Optional[List[T]]:
        pass
    
    @abstractmethod
    async def exists(self, values: T) -> bool:
        pass
    
    @abstractmethod
    async def update(self, id_: ValueObject, values: T) -> None:
        pass
