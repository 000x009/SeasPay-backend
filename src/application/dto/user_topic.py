from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional


@dataclass(frozen=True)
class UserTopicDTO:
    user_id: int
    supergroup_chat_id: int
    thread_id: int
    created_at: Optional[datetime] = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class CreateUserTopicDTO:
    user_id: int
    supergroup_chat_id: int
    username: str
    thread_id: int
    created_at: Optional[datetime] = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class GetUserTopicDTO:
    thread_id: int


@dataclass(frozen=True)
class GetUserTopicByUserIdDTO:
    user_id: int
