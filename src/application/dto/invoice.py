from dataclasses import dataclass
from datetime import datetime

from src.domain.value_objects.invoice import InvoiceStatus


@dataclass(frozen=True)
class InvoiceDTO:
    id: str
    order_id: int
    status: InvoiceStatus
    created_at: datetime


@dataclass(frozen=True)
class GetInvoiceDTO:
    id: str
    user_id: int


@dataclass(frozen=True)
class UpdateInvoiceDTO:
    id: str
    status: InvoiceStatus
