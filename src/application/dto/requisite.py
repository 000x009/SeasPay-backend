from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import List

from src.domain.value_objects.requisite import RequisiteTypeEnum
from src.application.common.dto import Pagination


@dataclass(frozen=True)
class RequisiteDTO:
    id: UUID
    user_id: int
    type: RequisiteTypeEnum
    created_at: datetime


@dataclass(frozen=True)
class RequisiteListResultDTO:
    requisites: List[RequisiteDTO]
    total: int


@dataclass(frozen=True)
class RequisiteListDTO:
    user_id: int
    pagination: Pagination


@dataclass(frozen=True)
class GetRequisiteDTO:
    requisite_id: UUID
