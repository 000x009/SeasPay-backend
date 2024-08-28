from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from aiogram.utils.web_app import WebAppInitData

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.services.order import OrderService
from src.presentation.dependencies.user_init_data import user_init_data_provider
from src.application.dto.order import OrderDTO, ListOrderDTO, GetOrderDTO, CreateOrderDTO
from src.application.common.dto import Pagination
from src.presentation.schema.order import CreateOrderSchema

router = APIRouter(
    prefix='/api/order',
    tags=['Order'],
    route_class=DishkaRoute,
)


@router.get('/')
async def get_order_list(
    limit: int,
    offset: int,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> Optional[List[OrderDTO]]:
    response = await order_service.list_(
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
async def get_order(
    order_id: int,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> Optional[OrderDTO]:
    response = await order_service.get(
        GetOrderDTO(
            user_id=user_data.user.id,
            order_id=order_id,
        )
    )

    return response


@router.put('/')
async def create_order(
    data: CreateOrderSchema,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> JSONResponse:
    await order_service.create(
        CreateOrderDTO(
            user_id=user_data.user.id,
            invoice_id=data.invoice_id,
            payment_receipt=data.payment_receipt,
            final_amount=data.final_amount,
            time=data.time,
            status=data.status,
        )
    )

    return JSONResponse(
        status_code=200,
        content={"message": "success"}
    )
