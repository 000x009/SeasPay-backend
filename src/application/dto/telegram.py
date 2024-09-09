from dataclasses import dataclass, field
from typing import Optional

from src.application.common.dto import File


@dataclass(frozen=True)
class SendOrderDTO:
    user_id: int
    username: str
    order_id: int
    order_text: str
    photo: Optional[File] = field(default=None)
