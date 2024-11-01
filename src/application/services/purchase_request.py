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
from src.application.dto.purchase_request import (
    PurchaseRequestDTO,
    CreatePurchaseRequestDTO,
    GetOnePurchaseRequestDTO,
    TakePurchaseRequestDTO,
    CancelPurchaseRequestDTO,
    ConfirmPurchaseRequestDTO,
)
from src.domain.value_objects.order_message import MessageID
from src.application.services.telegram_service import TelegramService
from src.application.dto.telegram import SendPurchaseRequestMessageDTO
from src.infrastructure.json_text_getter import get_purchase_request_text
from src.application.common.uow import UoW
from src.domain.exceptions.purchase_request import PurchaseRequestNotFound, PurchaseRequestAlreadyTaken
from src.application.services.product_application import ProductApplicationService
from src.application.dto.product_application import CreateProductApplicationDTO
from src.domain.entity.product_application import ProductApplicationStatusEnum


class PurchaseRequestService:
    def __init__(
        self,
        dal: PurchaseRequestDalImpl,
        telegram_service: TelegramService,
        product_application_service: ProductApplicationService,
        uow: UoW,
    ) -> None:
        self.dal = dal
        self.telegram_service = telegram_service
        self.uow = uow
        self.product_application_service = product_application_service
    
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
        request.message_id = MessageID(telegram_message.message_id)
        await self.dal.update(request)
        await self.uow.commit()

        return PurchaseRequestDTO(
            id=request.id.value,
            user_id=request.user_id.value,
            purchase_url=request.purchase_url.value,
            created_at=request.created_at.value,
            status=request.status.value,
            message_id=request.message_id.value if request.message_id else None,
        )

    async def get_request(self, data: GetOnePurchaseRequestDTO) -> PurchaseRequestDTO:
        request = await self.dal.get_one(PurchaseRequestId(data.id))
        if request is None:
            raise PurchaseRequestNotFound(f"Purchase request not found with id: {data.id}")
        
        return PurchaseRequestDTO(
            id=request.id.value,
            user_id=request.user_id.value,
            purchase_url=request.purchase_url.value,
            created_at=request.created_at.value,
            status=request.status.value,
            message_id=request.message_id.value if request.message_id else None,
        )
    
    async def take_request(self, data: TakePurchaseRequestDTO) -> PurchaseRequestDTO:
        request = await self.dal.get_one(PurchaseRequestId(data.id))
        if request is None:
            raise PurchaseRequestNotFound(f"Purchase request not found with id: {data.id}")
        if request.status.value != RequestStatusEnum.PENDING:
            raise PurchaseRequestAlreadyTaken(f"Purchase request with id: {data.id} already taken")

        return PurchaseRequestDTO(
            id=request.id.value,
            user_id=request.user_id.value,
            purchase_url=request.purchase_url.value,
            created_at=request.created_at.value,
            status=request.status.value,
            message_id=request.message_id.value if request.message_id else None,
        )

    async def cancel_request(self, data: CancelPurchaseRequestDTO) -> PurchaseRequestDTO:
        request = await self.dal.get_one(PurchaseRequestId(data.request_id))
        if request is None:
            raise PurchaseRequestNotFound(f"Purchase request not found with id: {data.request_id}")

        request.status = PurchaseRequestStatus(RequestStatusEnum.CANCELLED)
        await self.dal.update(request)
        await self.uow.commit()

        return PurchaseRequestDTO(
            id=request.id.value,
            user_id=request.user_id.value,
            purchase_url=request.purchase_url.value,
            created_at=request.created_at.value,
            status=request.status.value,
            message_id=request.message_id.value if request.message_id else None,
        )

    async def confirm_request(self, data: ConfirmPurchaseRequestDTO) -> PurchaseRequestDTO:
        request = await self.dal.get_one(PurchaseRequestId(data.request_id))
        if request is None:
            raise PurchaseRequestNotFound(f"Purchase request not found with id: {data.request_id}")

        request.status = PurchaseRequestStatus(RequestStatusEnum.CONFIRMED)
        await self.dal.update(request)
        await self.product_application_service.create_application(CreateProductApplicationDTO(
            user_id=request.user_id.value,
            purchase_request_id=request.id.value,
            required_fields=data.login_fields,
            status=ProductApplicationStatusEnum.SENT,
        ))
        await self.uow.commit()

        return PurchaseRequestDTO(
            id=request.id.value,
            user_id=request.user_id.value,
            purchase_url=request.purchase_url.value,
            created_at=request.created_at.value,
            status=request.status.value,
            message_id=request.message_id.value if request.message_id else None,
        )
