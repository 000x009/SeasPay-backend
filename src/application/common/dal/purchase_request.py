from abc import abstractmethod
from typing import Protocol, Optional, List

from src.domain.entity.purchase_request import PurchaseRequest
from src.domain.value_objects.purchase_request import PurchaseRequestId
from src.domain.value_objects.user import UserID


class PurchaseRequestDal(Protocol):
    @abstractmethod
    async def insert(self, purchase_request: PurchaseRequest) -> PurchaseRequest:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, request_id: PurchaseRequestId) -> Optional[PurchaseRequest]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: UserID) -> List[PurchaseRequest]:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> List[PurchaseRequest]:
        raise NotImplementedError
