from typing import List, Optional

from fastapi import APIRouter, Depends

from fastapi_redis_cache import cache

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.dto.feedback import (
    FeedbackDTO,
    ListInputDTO,
    GetFeedbackDTO,
    CreateFeedbackDTO,
    FeedbackListResultDTO
)
from src.application.services.feedback import FeedbackService
from src.presentation.web_api.schema.feedback import CreateFeedbackSchema
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider


router = APIRouter(
    tags=['Feedback'],
    prefix='/feedback',
    route_class=DishkaRoute,
)


@router.get('/', response_model=FeedbackListResultDTO)
@cache(expire=60)
async def get_feedback_list(
    page: int,
    feedback_service: FromDishka[FeedbackService],
) -> FeedbackListResultDTO:
    response = await feedback_service.list_feedbacks(ListInputDTO(page=page))

    return response


@router.get('/{feedback_id}')
@cache(expire=60)
async def get_feedback(
    feedback_id: int,
    feedback_service: FromDishka[FeedbackService],
) -> Optional[FeedbackDTO]:
    response = await feedback_service.get(
        GetFeedbackDTO(feedback_id=feedback_id),
    )

    return response


@router.post('/', response_model=FeedbackDTO)
async def post_feedback(
    data: CreateFeedbackSchema,
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> FeedbackDTO:
    response = await feedback_service.create(
        CreateFeedbackDTO(
            user_id=user_data.user.id,
            stars=data.stars,
            comment=data.comment,
            photo=data.photo,
        )
    )

    return response
