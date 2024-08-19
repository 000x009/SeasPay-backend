from typing import Optional

from datetime import datetime, UTC
from dataclasses import dataclass, field


@dataclass(frozen=True)
class UserDTO:
    user_id: int
    email: Optional[str] = field(default=None)
    joined_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True, kw_only=True)
class CreateUserDTO:
    user_id: int
    email: Optional[str] = field(default=None)
    joined_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class UpdateUserDTO:
    email: Optional[str] = field(default=None)
    joined_at: datetime = field(default=datetime.now(UTC))

