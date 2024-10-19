from fastapi import APIRouter, Depends

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.purchase_request import PurchaseRequestService
from src.application.dto.purchase_request import CreatePurchaseRequestDTO, PurchaseRequestDTO, GetUserPurchaseRequestsDTO
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
    # user_data: WebAppInitData = Depends(user_init_data_provider)
) -> PurchaseRequestDTO:
    return await purchase_request_service.send_request(CreatePurchaseRequestDTO(
        user_id=5297779345,
        purchase_url=data.purchase_url.__str__(),
        username='test'
    ))
