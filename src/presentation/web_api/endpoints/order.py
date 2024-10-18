from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, Body

from fastapi_redis_cache import cache

from aiogram.utils.web_app import WebAppInitData

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.services.order import OrderService
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.application.dto.order import (
    OrderDTO,
    ListOrderDTO,
    GetOrderDTO,
    CreateWithdrawOrderDTO,
    CreateTransferOrderDTO,
)
from src.application.common.dto import Pagination
from src.presentation.web_api.schema.order import CreateWithdrawOrderSchema, CreateTransferOrderSchema
from src.application.common.dto import FileDTO

router = APIRouter(
    prefix='/order',
    tags=['Order'],
    route_class=DishkaRoute,
)


@router.get('/')
@cache(expire=60 * 60 * 24)
async def get_order_list(
    limit: int,
    offset: int,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> Optional[List[OrderDTO]]:
    response = await order_service.list_orders(
        ListOrderDTO(
            user_id=user_data.user.id,
            pagination=Pagination(
                limit=limit,
                offset=offset,
            )
        )
    )

    return response


@router.get('/{order_id}')
@cache(expire=60 * 60 * 24)
async def get_order(
    order_id: UUID,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> Optional[OrderDTO]:
    response = await order_service.get(
        GetOrderDTO(
            order_id=order_id,
        )
    )

    return response


@router.post('/withdraw', response_model=OrderDTO)
async def create_withdraw_order(
    order_service: FromDishka[OrderService],
    data: CreateWithdrawOrderSchema = Body(),
    payment_receipt: UploadFile = File(),
) -> OrderDTO:
    response = await order_service.create_withdraw_order(
        CreateWithdrawOrderDTO(
            user_id=5297779345,
            created_at=data.created_at,
            status=data.status,
            withdraw_method=data.withdraw_method,
            receipt_photo=FileDTO(
                input_file=payment_receipt.file,
                filename=payment_receipt.filename,
            ),
            username='username',
        )
    )

    return response


@router.post('/transfer', response_model=OrderDTO)
async def create_transfer_order(
    order_service: FromDishka[OrderService],
    data: CreateTransferOrderSchema = Body(),
    payment_receipt: UploadFile = File(),
    # user_data: WebAppInitData = Depends(user_init_data_provider),
) -> OrderDTO:
    response = await order_service.create_transfer_order(
        CreateTransferOrderDTO(
            user_id=5297779345,
            receiver_email=data.receiver_email,
            username='some username',
            transfer_amount=data.amount,
            receipt_photo=FileDTO(
                input_file=payment_receipt.file,
                filename=payment_receipt.filename,
            ),
        )
    )

    return response
