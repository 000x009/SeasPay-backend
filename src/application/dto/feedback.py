from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, UTC


@dataclass(frozen=True)
class FeedbackDTO:
    id: int
    user_id: int
    stars: int
    comment: Optional[str] = field(default=None)
    created_at: datetime = field(default=datetime.now(UTC))


@dataclass
class ListInputDTO:
    limit: int
    offset: int


@dataclass
class GetFeedbackDTO:
    feedback_id: int


@dataclass
class CreateFeedbackDTO:
    user_id: int
    stars: int
    comment: Optional[str] = field(default=None)
    created_at: datetime = field(default=datetime.now(UTC))
