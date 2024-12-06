from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, UTC


@dataclass(frozen=True)
class FeedbackDTO:
    id: int
    user_id: int
    stars: int
    comment: Optional[str] = field(default=None)
    created_at: Optional[datetime] = field(default=datetime.now(UTC))
    photo: Optional[List[str]] = field(default=None)


@dataclass
class ListInputDTO:
    page: int


@dataclass
class GetFeedbackDTO:
    feedback_id: int


@dataclass
class CreateFeedbackDTO:
    user_id: int
    stars: int
    comment: Optional[str] = field(default=None)
    created_at: Optional[datetime] = field(default=datetime.now(UTC))
    photo: Optional[List[str]] = field(default=None)


@dataclass
class FeedbackListResultDTO:
    feedbacks: List[FeedbackDTO]
    total: int
