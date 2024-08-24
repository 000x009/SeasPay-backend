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
class UpdateUserDTO:
    joined_at: datetime = field(default=datetime.now(UTC))
    commission: int = field(default=15)
    total_withdrawn: Decimal = field(default=0)


@dataclass(frozen=True)
class GetUserDTO:
    user_id: int
