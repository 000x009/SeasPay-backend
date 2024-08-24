from abc import abstractmethod
from typing import Protocol, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.user import CreateUserDTO, GetUserDTO, UpdateUserDTO, UserDTO
from src.domain.value_objects.user import UserID
from src.domain.entity.user import User


class BaseUserDAL(Protocol):
    @abstractmethod
    async def insert(self, values: CreateUserDTO) -> None:
        pass

    @abstractmethod
    async def get_one(self, values: GetUserDTO) -> Optional[UserDTO]:
        pass

    @abstractmethod
    async def get_all(self, values: GetUserDTO) -> Optional[List[UserDTO]]:
        pass

    @abstractmethod
    async def exists(self, values: GetUserDTO) -> bool:
        pass

    # @abstractmethod
    # async def update(self, id_: UserID, values: User) -> None:
    #     pass
