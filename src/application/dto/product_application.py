from uuid import UUID
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Sequence, Dict

from src.domain.value_objects.product_application import ProductApplicationStatusEnum


@dataclass(frozen=True)
class ProductApplicationDTO:
    id: UUID
    user_id: int
    purchase_request_id: UUID
    created_at: datetime
    login_data: Sequence[str]
    status: ProductApplicationStatusEnum


@dataclass(frozen=True)
class CreateProductApplicationDTO:
    user_id: int
    purchase_request_id: UUID
    login_data: Sequence[str]
    created_at: datetime = field(default=datetime.now(UTC))
    status: ProductApplicationStatusEnum = field(default=ProductApplicationStatusEnum.SENT)


@dataclass(frozen=True)
class GetProductApplicationDTO:
    id: UUID


@dataclass(frozen=True)
class GetProductApplicationByRequestIdDTO:
    purchase_request_id: UUID


@dataclass(frozen=True)
class UpdateProductApplicationDTO:
    id: UUID
    login_data: Dict[str, str]
