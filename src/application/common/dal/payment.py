from typing import Protocol, Optional
from abc import abstractmethod

from src.domain.entity.payment import Payment
from src.domain.value_objects.payment import PaymentID


class PaymentDAL(Protocol):
    @abstractmethod
    async def get(self, payment_id: PaymentID) -> Optional[Payment]:
        raise NotImplementedError

    @abstractmethod
    async def insert(self, payment: Payment) -> Payment:
        raise NotImplementedError

    @abstractmethod
    async def update(self, payment: Payment) -> Payment:
        raise NotImplementedError
