from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from fastapi_redis_cache import cache

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.user import UserService
from src.application.dto.user import CreateUserDTO, GetUserDTO, UserDTO, UpdateUserCommissionDTO, UpdateUserTotalWithdrawnDTO
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.presentation.web_api.schema.user import CreateUserSchema, UpdateUserTotalWithdrawnSchema, UpdateUserCommissionSchema


router = APIRouter(
    prefix='/user',
    tags=['User'],
    route_class=DishkaRoute,
)


@router.post('/')
@cache(expire=60 * 60 * 24)
async def register_user(
    data: CreateUserSchema,
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_init_data_provider)
) -> UserDTO:
    response = await user_service.add(
        CreateUserDTO(
            user_id=user_data.user.id,
            joined_at=data.joined_at,
            commission=data.commission,
            total_withdrawn=data.total_withdrawn,
        )
    )

    return response


@router.get('/{user_id}')
@cache(expire=60 * 60 * 24)
async def get_user(
    user_id: int,
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> UserDTO:
    response = await user_service.get_user(GetUserDTO(user_id=user_id))

    return response
