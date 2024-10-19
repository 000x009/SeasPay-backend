import uuid

from src.infrastructure.dal.purchase_request import PurchaseRequestDalImpl
from src.domain.entity.purchase_request import PurchaseRequest
from src.domain.value_objects.purchase_request import (
    PurchaseRequestId,
    PurchaseURL,
    CreatedAt,
    PurchaseRequestStatus,
    RequestStatusEnum,
)
from src.domain.value_objects.user import UserID
from src.application.dto.purchase_request import(
    PurchaseRequestDTO,
    CreatePurchaseRequestDTO,
    GetUserPurchaseRequestsDTO,
    GetAllPurchaseRequestsDTO,
    GetOnePurchaseRequestDTO
)
from src.application.services.telegram_service import TelegramService
from src.application.dto.telegram import SendPurchaseRequestMessageDTO
from src.infrastructure.json_text_getter import get_purchase_request_text
from src.application.common.uow import UoW


class PurchaseRequestService:
    def __init__(
        self,
        dal: PurchaseRequestDalImpl,
        telegram_service: TelegramService,
        uow: UoW,
    ) -> None:
        self.dal = dal
        self.telegram_service = telegram_service
        self.uow = uow
    
    async def send_request(self, data: CreatePurchaseRequestDTO) -> PurchaseRequestDTO:
        request = PurchaseRequest(
            id=PurchaseRequestId(uuid.uuid4()),
            user_id=UserID(data.user_id),
            purchase_url=PurchaseURL(data.purchase_url),
            created_at=CreatedAt(data.created_at),
            status=PurchaseRequestStatus(RequestStatusEnum.PENDING),
        )
        await self.dal.insert(request)
        telegram_message = await self.telegram_service.send_purchase_request_message(
            SendPurchaseRequestMessageDTO(
                user_id=data.user_id,
                request_id=request.id.value,
                text=get_purchase_request_text(
                    request_id=request.id.value,
                    user_id=request.user_id.value,
                    purchase_url=request.purchase_url.value,
                    created_at=request.created_at.value,
                    status=request.status.value,
                ),
                username=data.username,
            )
        )
        await self.uow.commit()

        return PurchaseRequestDTO(
            id=PurchaseRequestId(request.id),
            user_id=UserID(request.user_id),
            purchase_url=PurchaseURL(request.purchase_url),
            created_at=CreatedAt(request.created_at),
            status=PurchaseRequestStatus(request.status),
        )

