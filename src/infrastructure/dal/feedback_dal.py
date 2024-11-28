from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.data.models import FeedbackModel
from src.domain.value_objects.feedback import FeedbackID, Stars, Comment, CreatedAt, Photo
from src.domain.value_objects.user import UserID
from src.domain.entity.feedback import Feedback, FeedbackDB
from src.application.common.dal.feedback import BaseFeedbackDAL


class FeedbackDAL(BaseFeedbackDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, feedback: Feedback) -> FeedbackDB:
        db_feedback = FeedbackModel(
            user_id=feedback.user_id.value,
            stars=feedback.stars.value,
            comment=feedback.comment.value,
            created_at=feedback.created_at.value,
            photo=feedback.photo.value if feedback.photo else None,
        )
        self._session.add(db_feedback)
        await self._session.flush(objects=[db_feedback])

        return FeedbackDB(
            id=FeedbackID(db_feedback.id),
            user_id=UserID(db_feedback.user_id),
            stars=Stars(db_feedback.stars),
            comment=Comment(db_feedback.comment),
            created_at=CreatedAt(db_feedback.created_at),
            photo=Photo(db_feedback.photo) if db_feedback.photo else None,
        )

    async def get(self, feedback_id: FeedbackID) -> Optional[FeedbackDB]:
        query = select(FeedbackModel).filter_by(id=feedback_id.value)
        result = await self._session.execute(query)
        db_feedback = result.scalar_one_or_none()

        if not db_feedback:
            return None

        return FeedbackDB(
            id=FeedbackID(db_feedback.id),
            user_id=UserID(db_feedback.user_id),
            stars=Stars(db_feedback.stars),
            comment=Comment(db_feedback.comment),
            created_at=CreatedAt(db_feedback.created_at),
            photo=Photo(db_feedback.photo) if db_feedback.photo else None,
        )

    async def list_(
        self,
        limit: int,
        offset: int,
    ) -> Optional[List[FeedbackDB]]:
        query = (
            select(FeedbackModel)
            .limit(limit + 1)
            .offset(offset)
            .order_by(FeedbackModel.created_at)
        )
        result = await self._session.execute(query)

        if result:
            db_feedbacks = result.scalars().all()
            return [
                FeedbackDB(
                    id=FeedbackID(db_feedback.id),
                    user_id=UserID(db_feedback.user_id),        
                    stars=Stars(db_feedback.stars),
                    comment=Comment(db_feedback.comment),
                    created_at=CreatedAt(db_feedback.created_at),
                    photo=Photo(db_feedback.photo) if db_feedback.photo else None,
                )
                for db_feedback in db_feedbacks
            ]
        else:
            return None
