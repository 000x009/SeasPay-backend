from uuid import UUID

from fastapi import APIRouter, Depends

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.requisite import RequisiteService
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.application.dto.requisite import (
    RequisiteDTO,
    RequisiteListDTO,
    GetRequisiteDTO,
    RequisiteListResultDTO,
)
from src.application.common.dto import Pagination

router = APIRouter(
    prefix='/requisite',
    tags=['Requisite'],
    route_class=DishkaRoute,
)

@router.get('/{id}')
async def get_one_requisite(
    id: UUID,
    requisite_service: FromDishka[RequisiteService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> RequisiteDTO:
    response = await requisite_service.get_requisite(
        GetRequisiteDTO(
            requisite_id=id,
            user_id=user_data.user.id,
        )
    )

    return response


@router.get('/')
async def list_requisites(
    limit: int,
    offset: int,
    requisite_service: FromDishka[RequisiteService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> RequisiteListResultDTO:
    response = await requisite_service.list_requisites(
        RequisiteListDTO(
            user_id=user_data.user.id,
            pagination=Pagination(
                limit=limit,
                offset=offset,
            )
        )
    )

    return response
