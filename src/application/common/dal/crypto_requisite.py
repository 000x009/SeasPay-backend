from typing import Protocol, Optional
from abc import abstractmethod

from src.domain.entity.crypto_requisite import CryptoRequisite
from src.domain.value_objects.requisite import RequisiteId


class CryptoRequisiteDAL(Protocol):
    @abstractmethod
    async def insert(self, crypto_requisite: CryptoRequisite) -> CryptoRequisite:
        raise NotImplementedError

    @abstractmethod 
    async def get(self, requisite_id: RequisiteId) -> Optional[CryptoRequisite]:
        raise NotImplementedError
