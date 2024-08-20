from typing import List, Optional

from src.infrastructure.dal import FeedbackDAL
from src.application.dto.feedback import FeedbackDTO, ListInputDTO, GetFeedbackDTO, CreateFeedbackDTO
from src.domain.value_objects.feedback import FeedbackID


class FeedbackService:
    def __init__(self, feedback_dal: FeedbackDAL):
        self._feedback_dal = feedback_dal

    async def list_(self, data: ListInputDTO) -> List[FeedbackDTO]:
        return await self._feedback_dal.list_(limit=data.limit, offset=data.offset)

    async def get(self, data: GetFeedbackDTO) -> Optional[FeedbackDTO]:
        return await self._feedback_dal.get_one(feedback_id=FeedbackID(data.feedback_id))

    async def create(self, data: CreateFeedbackDTO) -> None:
        await self._feedback_dal.insert(data=data)
