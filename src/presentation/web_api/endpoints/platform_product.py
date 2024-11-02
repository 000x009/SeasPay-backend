from typing import List

from fastapi import APIRouter

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.dto.platform_product import (
    PlatformProductDTO,
    GetPlatformProductDTO,
    ListPlatformProductDTO,
)
from src.application.services.platform_product import PlatformProductService
from src.application.common.dto import Pagination

router = APIRouter(
    prefix='/platform-product',
    tags=['Platform Product'],
    route_class=DishkaRoute,
)


@router.get('/{platform_id}/')
async def list_platform_products(
    platform_id: int,
    limit: int,
    offset: int,
    platform_product_service: FromDishka[PlatformProductService],
) -> List[PlatformProductDTO]:
    response = await platform_product_service.list_platform_product(
        ListPlatformProductDTO(
            platform_id=platform_id,
            pagination=Pagination(
                limit=limit,
                offset=offset,
            )
        )
    )

    return response


@router.get('/{id}')
async def get_platform_product(
    id: int,
    platform_product_service: FromDishka[PlatformProductService],
) -> PlatformProductDTO:
    response = await platform_product_service.get_platform_product(
        GetPlatformProductDTO(
            id=id,
        )
    )

    return response
