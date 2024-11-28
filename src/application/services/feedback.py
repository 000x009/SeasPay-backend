from typing import List

from src.infrastructure.dal import FeedbackDAL
from src.application.dto.feedback import FeedbackDTO, ListInputDTO, GetFeedbackDTO, CreateFeedbackDTO
from src.domain.value_objects.feedback import FeedbackID, Stars, Comment, CreatedAt, Photo
from src.domain.value_objects.user import UserID
from src.domain.entity.feedback import Feedback
from src.application.common.uow import UoW
from src.application.common.cloud_storage import CloudStorage
from src.domain.exceptions.feedback import FeedbackNotFoundError


class FeedbackService:
    def __init__(
        self,
        feedback_dal: FeedbackDAL,
        uow: UoW,
        cloud_storage: CloudStorage
    ):
        self._feedback_dal = feedback_dal
        self.uow = uow
        self.cloud_storage = cloud_storage

    async def list_(self, data: ListInputDTO) -> List[FeedbackDTO]:
        feedbacks = await self._feedback_dal.list_(limit=data.limit, offset=data.offset)
        if not feedbacks:
            raise FeedbackNotFoundError('Feedbacks not found')

        return [
            FeedbackDTO(
                id=feedback.id.value,
                user_id=feedback.user_id.value,
                stars=feedback.stars.value,
                comment=feedback.comment.value,
                created_at=feedback.created_at,
                photo=feedback.photo.value if feedback.photo else None,
            )
            for feedback in feedbacks
        ]

    async def get(self, data: GetFeedbackDTO) -> FeedbackDTO:
        feedback = await self._feedback_dal.get(feedback_id=FeedbackID(data.feedback_id))
        if feedback is None:
            raise FeedbackNotFoundError(f'Feedback with ID {data.feedback_id} not found')

        return FeedbackDTO(
            id=feedback.id.value,
            user_id=feedback.user_id.value,
            stars=feedback.stars.value,
            comment=feedback.comment.value,
            created_at=feedback.created_at.value,
            photo=feedback.photo.value,
        )
    
    async def create(self, data: CreateFeedbackDTO) -> FeedbackDTO:
        feedback = await self._feedback_dal.insert(Feedback(
            user_id=UserID(data.user_id),
            stars=Stars(data.stars),
            comment=Comment(data.comment),
            created_at=CreatedAt(data.created_at),
            photo=Photo(data.photo) if data.photo else None,
        ))
        await self.uow.commit()

        return FeedbackDTO(
            id=feedback.id.value,
            user_id=feedback.user_id.value,
            stars=feedback.stars.value,
            comment=feedback.comment.value,
            created_at=feedback.created_at.value,
            photo=feedback.photo.value if feedback.photo else None,
        )
