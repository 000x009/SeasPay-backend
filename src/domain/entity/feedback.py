from typing import Optional
from datetime import datetime, UTC

from src.domain.value_objects.user import UserID
from src.domain.value_objects.feedback import FeedbackID, Comment, CreatedAt, Stars


class Feedback:
    __slots__ = (
        'id',
        'user_id',
        'stars',
        'comment',
        'created_at',
    )

    def __init__(
        self,
        id: FeedbackID,
        user_id: UserID,
        stars: Stars,
        comment: Optional[Comment] = None,
        created_at: Optional[CreatedAt] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.stars = stars
        self.comment = comment
        self.created_at = created_at

        if self.created_at is None:
            self.created_at = datetime.now(UTC)
