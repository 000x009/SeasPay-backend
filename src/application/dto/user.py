from typing import Optional
from decimal import Decimal

from datetime import datetime, UTC
from dataclasses import dataclass, field


@dataclass(frozen=True)
class UserDTO:
    user_id: int
    joined_at: datetime = field(default=datetime.now(UTC))
    commission: int = field(default=15)
    total_withdrawn: Decimal = field(default=0)


@dataclass(frozen=True, kw_only=True)
class CreateUserDTO:
    user_id: int
    joined_at: datetime = field(default=datetime.now(UTC))
    commission: int = field(default=15)
    total_withdrawn: Decimal = field(default=0)


@dataclass(frozen=True)
class UpdateUserCommissionDTO:
    user_id: int
    commission: int


@dataclass(frozen=True)
class GetUserDTO:
    user_id: int


@dataclass(frozen=True)
class UpdateUserTotalWithdrawnDTO:
    user_id: int
    total_withdrawn: Decimal
