from abc import abstractmethod
from typing import Protocol, Optional, List

from src.domain.entity.requisite import Requisite
from src.domain.value_objects.requisite import RequisiteId
from src.domain.value_objects.user import UserID
from src.domain.value_objects.pagination import Limit, Offset


class RequisiteDAL(Protocol):
    @abstractmethod
    async def insert(self, requisite: Requisite) -> Requisite:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, requisite_id: RequisiteId) -> Optional[Requisite]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(
        self, user_id: UserID, limit: Limit, offset: Offset
    ) -> List[Requisite]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_total(self, user_id: UserID) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, requisite_id: RequisiteId) -> None:
        raise NotImplementedError
