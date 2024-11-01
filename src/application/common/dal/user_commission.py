from typing import Protocol, Optional
from abc import abstractmethod

from src.domain.entity.user_commission import UserCommission
from src.domain.value_objects.user import UserID


class UserCommissionDAL(Protocol):
    @abstractmethod
    async def get(self, user_id: UserID) -> Optional[UserCommission]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user_commission: UserCommission) -> UserCommission:
        raise NotImplementedError

    @abstractmethod
    async def insert(self, user_commission: UserCommission) -> UserCommission:
        raise NotImplementedError
