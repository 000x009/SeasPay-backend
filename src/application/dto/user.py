from decimal import Decimal

from datetime import datetime, UTC
from dataclasses import dataclass, field


@dataclass(frozen=True)
class UserDTO:
    user_id: int
    joined_at: datetime = field(default=datetime.now(UTC))
    total_withdrawn: Decimal = field(default=0)


@dataclass(frozen=True, kw_only=True)
class CreateUserDTO:
    user_id: int


@dataclass(frozen=True)
class UpdateUserDTO:
    user_id: int
    total_withdrawn: Decimal


@dataclass(frozen=True)
class UpdateUserCommissionDTO:
    user_id: int


@dataclass(frozen=True)
class GetUserDTO:
    user_id: int


@dataclass(frozen=True)
class UpdateUserTotalWithdrawnDTO:
    user_id: int
    total_withdrawn: Decimal


@dataclass(frozen=True)
class CalculateCommissionDTO:
    user_id: int
    paypal_received_amount: Decimal


@dataclass(frozen=True)
class CommissionDTO:
    commission: int
    user_must_receive: Decimal


@dataclass(frozen=True)
class NewUsersDTO:
    all: int
    month: int
    week: int
    day: int
