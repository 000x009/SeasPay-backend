from typing import Protocol
from abc import abstractmethod

from src.domain.entity.cryptopay import Invoice, ActiveInvoice


class CryptopayClient(Protocol):
    @abstractmethod
    async def create_invoice(self, invoice: Invoice) -> ActiveInvoice:
        raise NotImplementedError

    @abstractmethod
    async def get_exchange_rates(self, currency: str) -> dict:
        raise NotImplementedError
