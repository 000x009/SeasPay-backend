from typing import List, Optional

from fastapi import APIRouter, Depends, File, UploadFile, Body
from fastapi.responses import JSONResponse

from aiogram.utils.web_app import WebAppInitData

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.services.order import OrderService
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.application.dto.order import OrderDTO, ListOrderDTO, GetOrderDTO, CreateOrderDTO
from src.application.common.dto import Pagination
from src.presentation.web_api.schema.order import CreateOrderSchema
from src.application.common.dto import FileDTO

router = APIRouter(
    prefix='/order',
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


@router.post('/', response_model=OrderDTO)
async def create_order(
    order_service: FromDishka[OrderService],
    data: CreateOrderSchema = Body(),
    payment_receipt: UploadFile = File(),
) -> OrderDTO:
    response = await order_service.create(
        CreateOrderDTO(
            user_id=12823,
            payment_receipt="string",
            created_at=data.created_at,
            status=data.status,
            withdraw_method=data.withdraw_method,
            receipt_photo=FileDTO(
                input_file=payment_receipt.file.read(),
                filename=payment_receipt.filename,
            ),
        )
    )

    return response
