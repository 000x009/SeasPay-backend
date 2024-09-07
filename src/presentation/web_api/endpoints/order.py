from typing import List, Optional

from fastapi import APIRouter, Depends, File, UploadFile, Body
from fastapi.responses import JSONResponse

from aiogram.utils.web_app import WebAppInitData

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.services.order import OrderService
from src.application.dto.user import GetUserDTO
from src.application.services.user import UserService
from src.presentation.web_api.dependencies.user_init_data import user_init_data_provider
from src.application.dto.order import OrderDTO, ListOrderDTO, GetOrderDTO, CreateOrderDTO
from src.application.common.dto import Pagination
from src.presentation.web_api.schema.order import CreateOrderSchema
from src.application.services.json_text_getter import get_paypal_withdraw_order_text
from src.application.services.telegram_order_sender import TelegramOrderSender
from src.application.dto.telegram import SendOrderDTO
from src.application.common.dto import File as FileDTO

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


@router.post('/', response_class=JSONResponse)
async def create_order(
    order_service: FromDishka[OrderService],
    telegram_order_sender: FromDishka[TelegramOrderSender],
    user_service: FromDishka[UserService],
    data: CreateOrderSchema = Body(),
    payment_receipt: UploadFile = File(),
    # user_data: WebAppInitData = Depends(user_init_data_provider),
) -> JSONResponse:
    order = await order_service.create(
        CreateOrderDTO(
            user_id=12823,
            payment_receipt="string",
            created_at=data.created_at,
            status=data.status,
        )
    )
    user = await user_service.get_user(GetUserDTO(user_id=12823))
    await telegram_order_sender.send_order(
        SendOrderDTO(
            user_id=12823,
            order_text=get_paypal_withdraw_order_text(
                order_id=order.id,
                user_id=order.user_id,
                username=12823,
                created_at=order.created_at,
                status=order.status,
                commission=user.commission,
            ),
            username="some username",
            photo=FileDTO(
                input_file=payment_receipt.file.read(),
                filename=payment_receipt.filename,
            ) if payment_receipt is not None else None,
        )
    )

    return JSONResponse(
        status_code=200,
        content={"message": "success"}
    )
