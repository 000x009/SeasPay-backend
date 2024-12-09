from typing import Protocol
from abc import abstractmethod

from aiocryptopay.models.rates import ExchangeRate

from src.domain.entity.cryptopay import Invoice, ActiveInvoice


class CryptopayClient(Protocol):
    @abstractmethod
    async def create_invoice(self, invoice: Invoice) -> ActiveInvoice:
        raise NotImplementedError

    @abstractmethod
    async def get_rub_usd_rate(self) -> ExchangeRate:
        raise NotImplementedError
