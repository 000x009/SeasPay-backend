from uuid import UUID

from fastapi import APIRouter

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.dto.product_application import (
    ProductApplicationDTO,
    GetProductApplicationDTO,
)
from src.application.services.product_application import ProductApplicationService


router = APIRouter(
    prefix='/product_application',
    tags=['Product Application'],
    route_class=DishkaRoute,
)


@router.get('/{application_id}')
async def get_product_application(
    application_id: UUID,
    application_service: FromDishka[ProductApplicationService],
) -> ProductApplicationDTO:
    response = await application_service.get_application_by_id(GetProductApplicationDTO(
        id=application_id,
    ))

    return response
