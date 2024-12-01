from dataclasses import dataclass, field
from typing import Optional

from src.domain.value_objects.requisite import RequisiteTypeEnum


@dataclass(frozen=True)
class CryptoRequisiteDTO:
    requisite_id: int
    wallet_address: str
    asset: str
    network: str
    memo: Optional[str] = field(default=None)
    type: RequisiteTypeEnum = field(default=RequisiteTypeEnum.CRYPTO)


@dataclass(frozen=True)
class CryptoRequisiteCreateDTO:
    user_id: int
    wallet_address: str
    asset: str
    network: str
    memo: Optional[str] = field(default=None)


@dataclass(frozen=True)
class GetCryptoRequisiteDTO:
    requisite_id: int
