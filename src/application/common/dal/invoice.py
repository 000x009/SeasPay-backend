from typing import Protocol, Optional
from abc import abstractmethod

from src.domain.value_objects.invoice import InvoiceID
from src.domain.entity.invoice import Invoice


class BaseInvoiceDAL(Protocol):
    @abstractmethod
    async def get(self, invoice_id: InvoiceID) -> Optional[Invoice]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, invoice: Invoice) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, invoice_id: InvoiceID, invoice: Invoice) -> None:
        raise NotImplementedError
