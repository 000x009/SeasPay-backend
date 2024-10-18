from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from fastapi_redis_cache import cache

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.user import UserService
from src.application.dto.user import CreateUserDTO, GetUserDTO, UserDTO
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.presentation.web_api.schema.cloud import GetPresignedURLSchema


router = APIRouter(
    prefix='/cloud',
    tags=['Cloud'],
    route_class=DishkaRoute,
)


@router.get('/presigned_url')
async def get_object_pre_signed_url(
    data: GetPresignedURLSchema,
    # user_data: WebAppInitData = Depends(user_init_data_provider),
) -> JSONResponse:

