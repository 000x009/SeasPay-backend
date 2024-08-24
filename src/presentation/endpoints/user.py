from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.user import UserService
from src.application.dto.user import CreateUserDTO, GetUserDTO, UserDTO
from src.presentation.dependencies.user_init_data import user_init_data_provider
from src.presentation.schema.user import CreateUserSchema


router = APIRouter(
    tags=['User'],
    route_class=DishkaRoute,
)


@router.post('/')
async def register_user(
    data: CreateUserSchema,
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_init_data_provider)
) -> JSONResponse:
    await user_service.add(
        CreateUserDTO(
            user_id=user_data.user.id,
            joined_at=data.joined_at,
            commission=data.commission,
            total_withdrawn=data.total_withdrawn,
        )
    )

    return JSONResponse(content={"message": "success"}, status_code=200)


@router.get('/{user_id}')
async def get_user(
    user_id: int,
    user_service: FromDishka[UserService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> UserDTO:
    response = await user_service.get_user(GetUserDTO(user_id=user_id))

    return response
