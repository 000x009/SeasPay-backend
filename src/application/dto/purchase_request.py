from uuid import UUID
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Sequence
from decimal import Decimal

from src.application.common.dto import Pagination
from src.domain.value_objects.purchase_request import RequestStatusEnum


@dataclass(frozen=True)
class PurchaseRequestDTO:
    id: UUID
    user_id: int
    purchase_url: str
    message_id: int
    created_at: datetime = field(default=datetime.now(UTC))
    status: RequestStatusEnum = field(default=RequestStatusEnum.PENDING)


@dataclass(frozen=True)
class TakePurchaseRequestDTO:
    id: UUID


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


@dataclass(frozen=True)
class CancelPurchaseRequestDTO:
    request_id: UUID


@dataclass(frozen=True)
class ConfirmPurchaseRequestDTO:
    request_id: UUID
    login_fields: Sequence[str]
    price: Decimal
