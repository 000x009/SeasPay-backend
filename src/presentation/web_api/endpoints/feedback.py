from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File

from fastapi_redis_cache import cache

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.dto.feedback import FeedbackDTO, ListInputDTO, GetFeedbackDTO, CreateFeedbackDTO
from src.application.services.feedback import FeedbackService
from src.presentation.web_api.schema.feedback import CreateFeedbackSchema
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider


router = APIRouter(
    tags=['Feedback'],
    prefix='/feedback',
    route_class=DishkaRoute,
)


@router.get('/', response_model=List[FeedbackDTO])
@cache(expire=60 * 60 * 24)
async def get_feedback_list(
    limit: int,
    offset: int,
    feedback_service: FromDishka[FeedbackService],
    # user_data: WebAppInitData = Depends(user_init_data_provider),
) -> List[FeedbackDTO]:
    response = await feedback_service.list_(
        data=ListInputDTO(
            limit=limit,
            offset=offset,
        )
    )

    return response


@router.get('/{feedback_id}')
@cache(expire=60 * 60 * 24)
async def get_feedback(
    feedback_id: int,
    feedback_service: FromDishka[FeedbackService],
    # user_data: WebAppInitData = Depends(user_init_data_provider),
) -> Optional[FeedbackDTO]:
    response = await feedback_service.get(
        GetFeedbackDTO(feedback_id=feedback_id),
    )

    return response


@router.post('/', response_model=FeedbackDTO)
async def post_feedback(
    feedback_service: FromDishka[FeedbackService],
    data: CreateFeedbackSchema,
    # user_data: WebAppInitData = Depends(user_init_data_provider),
) -> FeedbackDTO:
    response = await feedback_service.create(
        CreateFeedbackDTO(
            user_id=5297779345,
            stars=data.stars,
            comment=data.comment,
            created_at=data.created_at,
            photo_url=data.photo_url,
        )
    )

    return response
