from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime
from typing import List, Optional

from src.domain.value_objects.requisite import RequisiteTypeEnum
from src.application.common.dto import Pagination


@dataclass(frozen=True)
class RequisiteDTO:
    id: UUID
    user_id: int
    type: RequisiteTypeEnum
    created_at: datetime


@dataclass(frozen=True)
class RequisiteReadDTO:
    id: UUID
    user_id: int
    type: RequisiteTypeEnum
    created_at: datetime


@dataclass(frozen=True)
class CardRequisiteListDTO(RequisiteReadDTO):
    number: str
    holder: str


@dataclass(frozen=True)
class CryptoRequisiteListDTO(RequisiteReadDTO):
    wallet_address: str
    network: str
    asset: str
    memo: Optional[str]


@dataclass(frozen=True)
class RequisiteListResultDTO:
    requisites: List[CryptoRequisiteListDTO | CardRequisiteListDTO]
    total: int


@dataclass(frozen=True)
class RequisiteListDTO:
    user_id: int
    pagination: Pagination


@dataclass(frozen=True)
class GetRequisiteDTO:
    requisite_id: UUID


@dataclass(frozen=True)
class CreateRequisiteDTO:
    user_id: int
    type: RequisiteTypeEnum
