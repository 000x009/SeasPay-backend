from abc import abstractmethod
from typing import Protocol, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto import UserDTO, UpdateUserDTO
from src.domain.value_objects.user.user_id import UserID


class BaseUserDAL(Protocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @abstractmethod
    async def insert(self, values: UserDTO) -> None:
        pass
    
    @abstractmethod  
    async def get_one(self, values: UserDTO) -> Optional[UserDTO]:
        pass
    
    @abstractmethod
    async def get_all(self, values: UserDTO) -> Optional[List[UserDTO]]:
        pass
    
    @abstractmethod
    async def exists(self, values: UserDTO) -> bool:
        pass
    
    @abstractmethod
    async def update(self, user_id: UserID, values: UpdateUserDTO) -> None:
        pass
    