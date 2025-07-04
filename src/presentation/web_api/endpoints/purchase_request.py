from uuid import UUID

from fastapi import APIRouter, Depends

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.purchase_request import PurchaseRequestService
from src.application.dto.purchase_request import CreatePurchaseRequestDTO, PurchaseRequestDTO, GetOnePurchaseRequestDTO
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.presentation.web_api.schema.purchase_request import CreatePurchaseRequestSchema


router = APIRouter(
    prefix='/purchase-request',
    tags=['Purchase Request'],
    route_class=DishkaRoute,
)


@router.post('/')
async def create_purchase_request(
    data: CreatePurchaseRequestSchema,
    purchase_request_service: FromDishka[PurchaseRequestService],
    user_data: WebAppInitData = Depends(user_init_data_provider)
) -> PurchaseRequestDTO:
    return await purchase_request_service.send_request(CreatePurchaseRequestDTO(
        user_id=user_data.user.id,
        purchase_url=data.purchase_url,
        username=user_data.user.username
    ))


@router.get('/{id}')
async def get_purchase_request(
    id: UUID,
    purchase_request_service: FromDishka[PurchaseRequestService],
    user_data: WebAppInitData = Depends(user_init_data_provider)
) -> PurchaseRequestDTO:
    return await purchase_request_service.get_request(GetOnePurchaseRequestDTO(id=id))
