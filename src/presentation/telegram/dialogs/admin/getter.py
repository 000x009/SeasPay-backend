from typing import Mapping

from aiogram_dialog import DialogManager

from dishka.integrations.aiogram import FromDishka

from src.application.services.order import OrderService
from src.application.dto.order import OrderDTO, ListOrderDTO, GetOrderDTO

from src.presentation.telegram.dialogs.common.injection import inject_getter
from src.infrastructure.json_text_getter import (
    get_order_info_card_text,
    get_order_info_crypto_text,
)
from src.domain.value_objects.withdraw_method import MethodEnum


@inject_getter
async def order_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    **kwargs
) -> Mapping[str, OrderDTO]:
    user_id = dialog_manager.start_data.get("user_id")
    orders = await order_service.list_orders(ListOrderDTO(user_id=12823))

    return {"orders": orders}


@inject_getter
async def one_order_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    **kwargs
) -> Mapping[str, OrderDTO]:
    order = await order_service.get(GetOrderDTO(order_id=int(dialog_manager.dialog_data.get("order_id"))))
    order_text = ""
    if order.withdraw_method.method == MethodEnum.CARD:
        order_text = get_order_info_card_text(
            order_id=order.id,
            user_id=order.user_id,
            commission=order.commission,
            created_at=order.created_at,
            status=order.status,
            card_number=order.withdraw_method.card_number,
            card_holder=order.withdraw_method.card_holder_name,
        )
    elif order.withdraw_method.method == MethodEnum.CRYPTO:
        order_text = get_order_info_crypto_text(
            order_id=order.id,
            user_id=order.user_id,
            commission=order.commission,
            created_at=order.created_at,
            status=order.status,
            address=order.withdraw_method.crypto_address,
            network=order.withdraw_method.crypto_network,
        )

    return {
        "order": order,
        "order_text": order_text,
    }
