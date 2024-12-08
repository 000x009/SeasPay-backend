from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from decimal import Decimal
from uuid import UUID

from aiocryptopay.const import CurrencyType as CryptoPayCurrencyType


@dataclass(frozen=True)
class InvoiceDTO:
    id: int
    payment_id: UUID
    url: str
    amount: Decimal
    currency_type: CryptoPayCurrencyType
    paid_amount: Decimal
    status: str
    paid_at: datetime
    expiration_date: datetime
    asset: Optional[str] = field(default=None)
    fiat: Optional[str] = field(default=None)


@dataclass(frozen=True)
class CreateInvoiceDTO:
    payment_id: UUID
    amount: Decimal
    currency_type: CryptoPayCurrencyType
    asset: Optional[str] = field(default=None)
    fiat: Optional[str] = field(default=None)
