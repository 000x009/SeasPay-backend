from uuid import UUID
from dataclasses import dataclass, field
from datetime import datetime, UTC

from src.application.common.dto import Pagination
from src.domain.value_objects.purchase_request import RequestStatusEnum


@dataclass(frozen=True)
class PurchaseRequestDTO:
    id: UUID
    user_id: int
    purchase_url: str
    created_at: datetime = field(default=datetime.now(UTC))
    status: RequestStatusEnum = field(default=RequestStatusEnum.PENDING)


@dataclass(frozen=True)
class CreatePurchaseRequestDTO:
    user_id: int
    purchase_url: str
    username: str
    created_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class GetUserPurchaseRequestsDTO:
    user_id: int
    pagination: Pagination


@dataclass(frozen=True)
class GetAllPurchaseRequestsDTO:
    pagination: Pagination


@dataclass(frozen=True)
class GetOnePurchaseRequestDTO:
    id: UUID
