from dataclasses import dataclass, field
from typing import Optional

from src.application.common.dto import File


@dataclass(frozen=True)
class SendMessageDTO:
    user_id: int
    username: str
    order_id: int
    text: str
    photo: Optional[File] = field(default=None)
