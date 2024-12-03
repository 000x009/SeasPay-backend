from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from aiogram.utils.web_app import WebAppInitData

from src.application.services.requisite import RequisiteService
from src.application.services.crypto_requisite import CryptoRequisiteService
from src.application.services.card_requisite import CardRequisiteService
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.application.dto.requisite import (
    RequisiteDTO,
    RequisiteListDTO,
    GetRequisiteDTO,
    RequisiteListResultDTO,
    DeleteRequisiteDTO,
)
from src.application.dto.crypto_requisite import CryptoRequisiteCreateDTO, CryptoRequisiteDTO
from src.application.dto.card_requisite import CardRequisiteCreateDTO, CardRequisiteDTO
from src.application.common.dto import Pagination
from src.presentation.web_api.schema.requisite import CreateCryptoRequisiteSchema, CreateCardRequisiteSchema

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
    response = await requisite_service.get_requisite(GetRequisiteDTO(requisite_id=id))

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


@router.delete('/{id}')
async def delete_requisite(
    id: UUID,
    requisite_service: FromDishka[RequisiteService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> JSONResponse:
    await requisite_service.delete_requisite(DeleteRequisiteDTO(requisite_id=id))

    return JSONResponse(status_code=200, content={"message": "success"})


@router.post('/crypto')
async def create_crypto_requisite(
    data: CreateCryptoRequisiteSchema,
    crypto_requisite_service: FromDishka[CryptoRequisiteService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> CryptoRequisiteDTO:
    response = await crypto_requisite_service.create(
        CryptoRequisiteCreateDTO(
            user_id=user_data.user.id,
            wallet_address=data.wallet_address,
            asset=data.asset,
            network=data.network,
            memo=data.memo,
        )
    )

    return response


@router.post('/card')
async def create_card_requisite(
    data: CreateCardRequisiteSchema,
    card_requisite_service: FromDishka[CardRequisiteService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> CardRequisiteDTO:
    response = await card_requisite_service.create(
        CardRequisiteCreateDTO(
            user_id=user_data.user.id,
            number=data.number,
            holder=data.holder,
        )
    )

    return response
