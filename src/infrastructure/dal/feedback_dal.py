from typing import Optional, List
from dataclasses import asdict

from sqlalchemy import insert, update, select, exists, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common import DAL
from src.application.dto.feedback import FeedbackDTO, GetFeedbackDTO, CreateFeedbackDTO
from src.infrastructure.data.models import FeedbackModel
from src.domain.value_objects.feedback import FeedbackID


class FeedbackDAL(DAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, data: CreateFeedbackDTO) -> None:
        query = insert(FeedbackModel).values(**asdict(data))
        await self._session.execute(query)
        await self._session.commit()

    async def update(self, id_: FeedbackID, values: FeedbackDTO) -> None:
        query = update(FeedbackModel).where(FeedbackModel.id == id_.value).values(**asdict(values))
        await self._session.execute(query)
        await self._session.commit()

    async def exists(self, values: FeedbackDTO) -> bool:
        query = select(
            exists().where(
                *(
                    getattr(FeedbackModel, key) == value
                    for key, value in asdict(values).items()
                    if hasattr(FeedbackModel, key)
                )
            )
        )
        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_one(self, feedback_id: FeedbackID) -> Optional[FeedbackDTO]:
        query = select(FeedbackModel).filter_by(id=feedback_id.value)
        result = await self._session.execute(query)

        if result:
            db_feedback = result.scalar_one()
            return FeedbackDTO(
                id=db_feedback.id,
                user_id=db_feedback.user_id,
                stars=db_feedback.stars,
                comment=db_feedback.comment,
                created_at=db_feedback.created_at,
            )

    async def list_(
        self,
        limit: int,
        offset: int,
    ) -> Optional[List[FeedbackDTO]]:
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
                FeedbackDTO(
                    id=db_feedback.id,
                    user_id=db_feedback.user_id,
                    stars=db_feedback.stars,
                    comment=db_feedback.comment,
                    created_at=db_feedback.created_at,
                )
                for db_feedback in db_feedbacks
            ]

    async def delete(self, values: FeedbackDTO) -> None:
        query = delete(FeedbackModel).filter_by(**asdict(values))
        await self._session.execute(query)
        await self._session.commit()
