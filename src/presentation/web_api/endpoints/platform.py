from fastapi import APIRouter

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.dto.platform import (
    PlatformDTO,
    GetPlatformDTO,
    ListPlatformDTO,
    PlatformListResultDTO
)
from src.application.services.platform import PlatformService
from src.application.common.dto import Pagination

router = APIRouter(
    prefix='/platform',
    tags=['Platform'],
    route_class=DishkaRoute,
)


@router.get('/')
async def list_platforms(
    limit: int,
    offset: int,
    platform_service: FromDishka[PlatformService],
) -> PlatformListResultDTO:
    response = await platform_service.list_platform(
        ListPlatformDTO(
            pagination=Pagination(
                limit=limit,
                offset=offset,
            )
        )
    )

    return response


@router.get('/{platform_id}')
async def get_platform(
    platform_id: int,
    platform_service: FromDishka[PlatformService],
) -> PlatformDTO:
    response = await platform_service.get_platform(
        GetPlatformDTO(
            platform_id=platform_id,
        )
    )

    return response
