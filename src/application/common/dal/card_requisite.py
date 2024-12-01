from typing import Protocol, Optional
from abc import abstractmethod

from src.domain.entity.card_requisite import CardRequisite
from src.domain.value_objects.requisite import RequisiteId


class CardRequisiteDAL(Protocol):
    @abstractmethod
    async def insert(self, card_requisite: CardRequisite) -> CardRequisite:
        raise NotImplementedError

    @abstractmethod 
    async def get(self, requisite_id: RequisiteId) -> Optional[CardRequisite]:
        raise NotImplementedError
