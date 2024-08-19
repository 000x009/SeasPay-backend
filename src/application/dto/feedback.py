from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, UTC


@dataclass(frozen=True)
class FeedbackDTO:
    id: int
    user_id: int
    order_id: int
    stars: int
    comment: Optional[str] = field(default=None)
    posted_at: datetime = field(default=datetime.now(UTC))

