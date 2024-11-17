from fastapi import APIRouter, Depends

from fastapi_redis_cache import cache

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.user import UserService
from src.application.dto.user import CreateUserDTO, GetUserDTO, UserDTO
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.presentation.web_api.schema.user import CreateUserSchema


router = APIRouter(
    prefix='/user',
    tags=['User'],
    route_class=DishkaRoute,
)


@router.post('/')
async def register_user(
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_init_data_provider)
) -> UserDTO:
    response = await user_service.add(CreateUserDTO(user_id=user_data.user.id))

    return response


@router.get('/')
@cache(expire=60)
async def get_user(
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> UserDTO:
    response = await user_service.get_user(GetUserDTO(user_id=user_data.user.id))

    return response
