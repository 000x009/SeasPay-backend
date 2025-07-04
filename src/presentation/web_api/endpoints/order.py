from uuid import UUID

from fastapi import APIRouter, Depends

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
    CreateDigitalProductOrderDTO,
    PurchasePlatformProductDTO,
    OrderListResultDTO,
)
from src.presentation.web_api.schema.order import (
    CreateWithdrawOrderSchema,
    CreateTransferOrderSchema,
    CreateDigitalProductOrderSchema,
    PurchasePlatformProductSchema,
)

router = APIRouter(
    prefix='/order',
    tags=['Order'],
    route_class=DishkaRoute,
)


@router.get('/')
@cache(expire=60)
async def get_order_list(
    page: int,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> OrderListResultDTO:
    response = await order_service.list_orders(
        ListOrderDTO(
            user_id=user_data.user.id,
            page=page,
        )
    )

    return response


@router.get('/{order_id}')
@cache(expire=60)
async def get_order(
    order_id: UUID,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> OrderDTO:
    response = await order_service.get(GetOrderDTO(order_id=order_id))

    return response


@router.post('/withdraw', response_model=OrderDTO)
async def create_withdraw_order(
    data: CreateWithdrawOrderSchema,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> OrderDTO:
    response = await order_service.create_withdraw_order(
        CreateWithdrawOrderDTO(
            user_id=user_data.user.id,
            requisite_id=data.requisite_id,
            payment_receipt_url=data.payment_receipt_url,
            username=user_data.user.username if user_data.user.username else user_data.user.first_name,
        )
    )

    return response


@router.post('/transfer', response_model=OrderDTO)
async def create_transfer_order(
    data: CreateTransferOrderSchema,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> OrderDTO:
    response = await order_service.create_transfer_order(
        CreateTransferOrderDTO(
            user_id=user_data.user.id,
            receiver_email=data.receiver_email,
            username=user_data.user.username if user_data.user.username else user_data.user.first_name,
            transfer_amount=data.amount,
            payment_receipt_url=data.payment_receipt_url,
            payment_id=data.payment_id,
        )
    )

    return response


@router.post('/digital-product', response_model=OrderDTO)
async def create_digital_product_order(
    data: CreateDigitalProductOrderSchema,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> OrderDTO:
    response = await order_service.create_digital_product_order(
        CreateDigitalProductOrderDTO(
            user_id=user_data.user.id,
            application_id=data.application_id,
            payment_receipt_url=data.payment_receipt_url,
            payment_id=data.payment_id,
            login_data=data.login_data,
            username=user_data.user.username if user_data.user.username else user_data.user.first_name,
        )
    )

    return response


@router.post('/platform-product', response_model=OrderDTO)
async def purchase_platform_product(
    data: PurchasePlatformProductSchema,
    order_service: FromDishka[OrderService],
    user_data: WebAppInitData = Depends(user_init_data_provider),
) -> OrderDTO:
    response = await order_service.purchase_platform_product(
        PurchasePlatformProductDTO(
            user_id=user_data.user.id,
            platform_product_id=data.product_id,
            payment_receipt_url=data.payment_receipt_url,
            payment_id=data.payment_id,
            login_data=data.login_data,
            username=user_data.user.username if user_data.user.username else user_data.user.first_name,
        )
    )

    return response
