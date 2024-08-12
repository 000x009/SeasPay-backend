from datetime import datetime, UTC
from dataclasses import dataclass, field


@dataclass
class UserDTO:
    user_id: int
    email: str
    joining_date: datetime = field(default=datetime.now(UTC))
