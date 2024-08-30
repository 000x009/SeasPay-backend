from typing import List, Optional

from src.infrastructure.dal import FeedbackDAL
from src.application.dto.feedback import FeedbackDTO, ListInputDTO, GetFeedbackDTO, CreateFeedbackDTO
from src.domain.value_objects.feedback import FeedbackID, Stars, Comment, CreatedAt
from src.domain.value_objects.user import UserID
from src.domain.entity.feedback import Feedback

class FeedbackService:
    def __init__(self, feedback_dal: FeedbackDAL):
        self._feedback_dal = feedback_dal

    async def list_(self, data: ListInputDTO) -> List[FeedbackDTO]:
        return await self._feedback_dal.list_(limit=data.limit, offset=data.offset)

    async def get(self, data: GetFeedbackDTO) -> Optional[FeedbackDTO]:
        feedback = await self._feedback_dal.get_one(feedback_id=FeedbackID(data.feedback_id))
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
            id=FeedbackID(data.feedback_id),
            user_id=UserID(data.user_id),
            stars=Stars(data.stars),
            comment=Comment(data.comment),
            created_at=CreatedAt(data.created_at),
        ))

        return FeedbackDTO(
            id=feedback.id.value,
            user_id=feedback.user_id.value,
            stars=feedback.stars.value,
            comment=feedback.comment.value,
            created_at=feedback.created_at.value,
        )
