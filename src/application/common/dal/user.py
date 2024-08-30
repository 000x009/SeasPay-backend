from abc import abstractmethod
from typing import Protocol, Optional, List

from src.domain.value_objects.user import UserID
from src.domain.entity.user import User


class BaseUserDAL(Protocol):
    @abstractmethod
    async def insert(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_one(self, user_id: UserID) -> Optional[User]:
        pass

    @abstractmethod
    async def get_all_users(self) -> Optional[List[User]]:
        pass

    @abstractmethod
    async def update(self, user_id: UserID, user: User) -> None:
        pass
