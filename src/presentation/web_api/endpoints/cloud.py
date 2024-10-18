from fastapi import APIRouter, Depends

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.cloud import CloudService
from src.application.dto.cloud import PresignedPostDTO, GetPresignedPostDTO


router = APIRouter(
    prefix='/cloud',
    tags=['Cloud'],
    route_class=DishkaRoute,
)


@router.get('/presigned-post/{filename}')
async def get_presigned_post(
    filename: str,
    cloud_service: FromDishka[CloudService],
    # user_data: WebAppInitData = Depends(user_init_data_provider),
) -> PresignedPostDTO:
    response = cloud_service.get_object_presigned_post(
        GetPresignedPostDTO(
            filename=filename,
        )
    )

    return response
