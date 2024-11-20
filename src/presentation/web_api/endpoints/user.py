from fastapi import APIRouter, Depends

from fastapi_redis_cache import cache

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.user import UserService
from src.application.dto.user import CreateUserDTO, GetUserDTO, UserDTO, ShareReferralDTO, LoginDTO, ReferralDTO
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider


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
    print(user_data.start_param)
    response = await user_service.get_user(GetUserDTO(user_id=user_data.user.id))

    return response


@router.get('/share-referral/')
@cache(expire=60 * 60 * 24)
async def share_referral(
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> ReferralDTO:
    response = await user_service.share_referral(ShareReferralDTO(user_id=user_data.user.id))

    return response


@router.post('/login/')
@cache(expire=60)
async def login(
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_init_data_provider)
) -> UserDTO:
    print(user_data.start_param, flush=True)
    response = await user_service.login(
        LoginDTO(
            user_id=user_data.user.id,
            referral_id=user_data.start_param,
        )
    )

    return response
