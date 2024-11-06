from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List

from src.application.common.dto import Pagination


@dataclass(frozen=True)
class PlatformProductDTO:
    id: int
    platform_id: int
    purchase_url: str
    price: Decimal
    name: str
    image_url: str
    instruction: Optional[str] = field(default=None)


@dataclass(frozen=True)
class AddPlatformProductDTO:
    platform_id: int
    purchase_url: str
    price: Decimal
    image_url: str
    name: str
    instruction: Optional[str] = field(default=None)


@dataclass(frozen=True)
class GetPlatformProductDTO:
    id: int


@dataclass(frozen=True)
class DeletePlatformProductDTO:
    id: int


@dataclass(frozen=True)
class ListPlatformProductDTO:
    platform_id: int
    pagination: Pagination


@dataclass(frozen=True)
class ListPlatformProductResultDTO:
    total: int
    products: List[PlatformProductDTO]


@dataclass(frozen=True)
class PurchasePlatformProductDTO:
    product_id: int



@dataclass(frozen=True)
class UpdatePlatformProductDTO:
    platform_id: int
    product_id: int
    purchase_url: str
    price: Decimal
    image_url: str
    name: str
    instruction: Optional[str] = field(default=None)
