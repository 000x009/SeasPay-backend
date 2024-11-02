from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from src.application.common.dto import Pagination


@dataclass(frozen=True)
class PlatformProductDTO:
    id: int
    platform_id: int
    purchase_url: str
    price: Decimal
    image_url: str
    instruction: Optional[str] = field(default=None)


@dataclass(frozen=True)
class GetPlatformProductDTO:
    id: int


@dataclass(frozen=True)
class ListPlatformProductDTO:
    platform_id: int
    pagination: Pagination
