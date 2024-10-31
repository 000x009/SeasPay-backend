from uuid import UUID
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, List

from src.domain.value_objects.product_application import ProductApplicationStatusEnum



@dataclass(frozen=True)
class ProductApplicationDTO:
    id: UUID
    user_id: int
    purchase_request_id: UUID
    created_at: datetime
    required_fields: Dict[str, List[str]]
    status: ProductApplicationStatusEnum


@dataclass(frozen=True)
class CreateProductApplicationDTO:
    user_id: int
    purchase_request_id: UUID
    required_fields: Dict[str, List[str]]
    created_at: datetime = field(default=datetime.now(UTC))
    status: ProductApplicationStatusEnum = field(default=ProductApplicationStatusEnum.SENT)


@dataclass(frozen=True)
class GetProductApplicationDTO:
    id: UUID
