from typing import Optional
from datetime import datetime, UTC

from src.domain.value_objects.user import UserID
from src.domain.value_objects.feedback import FeedbackID, Comment, CreatedAt, Stars, Photo


class Feedback:
    __slots__ = (
        'user_id',
        'stars',
        'comment',
        'created_at',
        'photo',
    )

    def __init__(
        self,
        user_id: UserID,
        stars: Stars,
        comment: Optional[Comment] = None,
        created_at: Optional[CreatedAt] = None,
        photo: Optional[Photo] = None,
    ) -> None:
        self.user_id = user_id
        self.stars = stars
        self.comment = comment
        self.created_at = created_at
        self.photo = photo

        if self.created_at is None:
            self.created_at = datetime.now(UTC)


class FeedbackDB(Feedback):
    __slots__ = ('id',)

    def __init__(
        self,
        id: FeedbackID,
        user_id: UserID,
        stars: Stars,
        comment: Optional[Comment] = None,
        created_at: Optional[CreatedAt] = None,
        photo: Optional[Photo] = None,
    ) -> None:
        self.id = id
        super().__init__(
            user_id, stars, comment, created_at, photo
        )
