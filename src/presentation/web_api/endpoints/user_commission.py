from decimal import Decimal

from fastapi import APIRouter, Depends
from fastapi_redis_cache import cache

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.user_commission import UserCommissionService
from src.application.dto.user_commission import (
    UserCommissionDTO,
    GetUserCommissionDTO,
    CountCommissionDTO,
    CountCommissionResultDTO,
)
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider


router = APIRouter(
    prefix='/user-commission',
    tags=['User Commission'],
    route_class=DishkaRoute,
)


@router.get('/')
@cache(expire=60)
async def get_user_commission(
    user_commission_service: FromDishka[UserCommissionService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> UserCommissionDTO:
    return await user_commission_service.get(GetUserCommissionDTO(user_id=user_data.user.id))


@router.get('/count-commission')
async def count_commission(
    amount: Decimal,
    user_commission_service: FromDishka[UserCommissionService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> CountCommissionResultDTO:
    response = await user_commission_service.count_commission(
        CountCommissionDTO(
            amount=amount,
            user_id=user_data.user.id,
        )
    )

    return response
