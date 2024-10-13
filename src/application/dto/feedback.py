from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, UTC
from src.application.dto.order import FileDTO


@dataclass(frozen=True)
class FeedbackDTO:
    id: int
    user_id: int
    stars: int
    comment: Optional[str] = field(default=None)
    created_at: Optional[datetime] = field(default=datetime.now(UTC))
    photo_url: Optional[str] = field(default=None)


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
    created_at: Optional[datetime] = field(default=datetime.now(UTC))
    photo: Optional[FileDTO] = field(default=None)
