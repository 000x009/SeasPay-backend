from uuid import UUID
from decimal import Decimal

from typing import Dict
from dataclasses import dataclass


@dataclass(frozen=True)
class DigitalProductDetailsDTO:
    order_id: UUID
    purchase_url: str
    commission: Decimal
    login_data: Dict[str, str]


@dataclass(frozen=True)
class GetDigitalProductDetailsDTO:
    order_id: UUID
