from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal.purchase_request import PurchaseRequestDal
from src.infrastructure.data.models import PurchaseRequestModel
from src.domain.entity.purchase_request import PurchaseRequest
from src.domain.value_objects.purchase_request import (
    PurchaseRequestId,
    PurchaseURL,
    CreatedAt,
    PurchaseRequestStatus,
    MessageID,
)
from src.domain.value_objects.user import UserID


class PurchaseRequestDalImpl(PurchaseRequestDal):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, purchase_request: PurchaseRequest) -> PurchaseRequest:
        request_model = PurchaseRequestModel(
            id=purchase_request.id.value,
            user_id=purchase_request.user_id.value,
            purchase_url=purchase_request.purchase_url.value,
            created_at=purchase_request.created_at.value,
            status=purchase_request.status.value,
            telegram_message_id=purchase_request.message_id.value if purchase_request.message_id else None,
        )
        self.session.add(request_model)

        return purchase_request

    async def update(self, purchase_request: PurchaseRequest) -> PurchaseRequest:
        request_model = PurchaseRequestModel(
            id=purchase_request.id.value,
            user_id=purchase_request.user_id.value,
            purchase_url=purchase_request.purchase_url.value,
            created_at=purchase_request.created_at.value,
            status=purchase_request.status.value,
            telegram_message_id=purchase_request.message_id.value,
        )
        await self.session.merge(request_model)

        return purchase_request

    async def get_one(self, request_id: PurchaseRequestId) -> Optional[PurchaseRequest]:
        query = select(PurchaseRequestModel).where(PurchaseRequestModel.id == request_id.value)
        result = await self.session.execute(query)
        request_model = result.scalar_one_or_none()
        if request_model is None:
            return None
        
        return PurchaseRequest(
            id=PurchaseRequestId(request_model.id),
            user_id=UserID(request_model.user_id),
            purchase_url=PurchaseURL(request_model.purchase_url),
            created_at=CreatedAt(request_model.created_at),
            status=PurchaseRequestStatus(request_model.status),
            message_id=MessageID(request_model.telegram_message_id) if request_model.telegram_message_id else None,
        )

    async def list_by_user(self, user_id: UserID, limit: int, offset: int) -> List[PurchaseRequest]:
        query = select(PurchaseRequestModel).where(PurchaseRequestModel.user_id == user_id.value).limit(limit).offset(offset)
        result = await self.session.execute(query)
        request_models = result.scalars().all()

        return [
            PurchaseRequest(
                id=PurchaseRequestId(request_model.id),
                user_id=UserID(request_model.user_id),
                purchase_url=PurchaseURL(request_model.purchase_url),
                created_at=CreatedAt(request_model.created_at),
                status=PurchaseRequestStatus(request_model.status),
                message_id=MessageID(request_model.telegram_message_id) if request_model.telegram_message_id else None,
            )
            for request_model in request_models
        ]

    async def list_all(self, limit: int, offset: int) -> List[PurchaseRequest]:
        query = select(PurchaseRequestModel).limit(limit).offset(offset)
        result = await self.session.execute(query)
        request_models = result.scalars().all()

        return [
            PurchaseRequest(
                id=PurchaseRequestId(request_model.id),
                user_id=UserID(request_model.user_id),
                purchase_url=PurchaseURL(request_model.purchase_url),
                created_at=CreatedAt(request_model.created_at),
                status=PurchaseRequestStatus(request_model.status),
                message_id=MessageID(request_model.telegram_message_id) if request_model.telegram_message_id else None,
            )
            for request_model in request_models
        ]

