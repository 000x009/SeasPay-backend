from typing import List, Optional

from src.infrastructure.dal import FeedbackDAL
from src.application.dto.feedback import FeedbackDTO, ListInputDTO, GetFeedbackDTO, CreateFeedbackDTO
from src.domain.value_objects.feedback import FeedbackID, Stars, Comment, CreatedAt
from src.domain.value_objects.user import UserID
from src.domain.entity.feedback import Feedback
from src.application.common.uow import UoW


class FeedbackService:
    def __init__(
        self,
        feedback_dal: FeedbackDAL,
        uow: UoW,
    ):
        self._feedback_dal = feedback_dal
        self.uow = uow

    async def list_(self, data: ListInputDTO) -> List[FeedbackDTO]:
        feedbacks = await self._feedback_dal.list_(limit=data.limit, offset=data.offset)

        return [
            FeedbackDTO(
                id=feedback.id.value,
                user_id=feedback.user_id.value,
                stars=feedback.stars.value,
                comment=feedback.comment.value,
                created_at=feedback.created_at,
            )
            for feedback in feedbacks
        ]

    async def get(self, data: GetFeedbackDTO) -> Optional[FeedbackDTO]:
        feedback = await self._feedback_dal.get(feedback_id=FeedbackID(data.feedback_id))
        if feedback is None:
            return None

        return FeedbackDTO(
            id=feedback.id.value,
            user_id=feedback.user_id.value,
            stars=feedback.stars.value,
            comment=feedback.comment.value,
            created_at=feedback.created_at.value,
        )
    
    async def create(self, data: CreateFeedbackDTO) -> FeedbackDTO:
        feedback = await self._feedback_dal.insert(Feedback(
            user_id=UserID(data.user_id),
            stars=Stars(data.stars),
            comment=Comment(data.comment),
            created_at=CreatedAt(data.created_at),
        ))
        await self.uow.commit()

        return FeedbackDTO(
            id=feedback.id.value,
            user_id=feedback.user_id.value,
            stars=feedback.stars.value,
            comment=feedback.comment.value,
            created_at=feedback.created_at.value,
        )
