from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class DAL(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @abstractmethod
    async def insert(self) -> None:
        pass

    @abstractmethod  
    async def get_one(self):
        pass
    
    @abstractmethod
    async def get_all(self):
        pass
    
    @abstractmethod
    async def exists(self) -> bool:
        pass
    
    @abstractmethod
    async def update(self) -> None:
        pass
    