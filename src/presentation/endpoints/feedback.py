from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.dto.feedback import FeedbackDTO, ListInputDTO, GetFeedbackDTO, CreateFeedbackDTO
from src.application.services.feedback import FeedbackService
from src.presentation.schema.feedback import CreateFeedback
from src.presentation.dependencies.user_init_data import user_init_data_provider


router = APIRouter(
    tags=['Feedback'],
    prefix='/feedback',
    route_class=DishkaRoute,
)


@router.get('/', response_model=List[FeedbackDTO])
async def get_feedback_list(
    limit: int,
    offset: int,
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> List[FeedbackDTO]:
    response = await feedback_service.list_(
        data=ListInputDTO(
            limit=limit,
            offset=offset,
        )
    )

    return response


@router.get('/{feedback_id}')
async def get_feedback(
    feedback_id: int,
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> Optional[FeedbackDTO]:
    response = await feedback_service.get(
        GetFeedbackDTO(feedback_id=feedback_id),
    )

    return response


@router.post('/', response_class=JSONResponse)
async def post_feedback(
    data: CreateFeedback,
    feedback_service: FromDishka[FeedbackService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> JSONResponse:
    await feedback_service.create(
        CreateFeedbackDTO(
            user_id=user_data.user.id,
            stars=data.stars,
            comment=data.comment,
            created_at=data.created_at,
        )
    )

    return JSONResponse(
        status_code=200,
        content={"message": "success"},
    )
