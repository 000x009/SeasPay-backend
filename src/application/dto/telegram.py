from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from src.application.common.dto import FileDTO


@dataclass(frozen=True)
class SendMessageDTO:
    user_id: int
    username: str
    order_id: UUID
    text: str
    photo: Optional[FileDTO] = field(default=None)
