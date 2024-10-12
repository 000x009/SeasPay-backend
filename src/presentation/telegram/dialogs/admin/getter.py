from typing import Mapping, Dict

from aiogram_dialog import DialogManager

from dishka.integrations.aiogram import FromDishka

from src.application.services.order import OrderService
from src.application.services.user import UserService
from src.application.dto.order import OrderDTO, ListOrderDTO, GetOrderDTO
from src.application.dto.user import GetUserDTO, UserDTO

from src.presentation.telegram.dialogs.common.injection import inject_getter
from src.infrastructure.json_text_getter import (
    get_order_info_card_text,
    get_order_info_crypto_text,
    get_user_profile_text,
)
from src.domain.value_objects.withdraw_method import MethodEnum


@inject_getter
async def order_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    **kwargs
) -> Mapping[str, list[OrderDTO]]:
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
    if order and order.withdraw_method.method == MethodEnum.CARD:
        order_text = get_order_info_card_text(
            order_id=order.id,
            user_id=order.user_id,
            commission=order.commission,
            created_at=order.created_at,
            status=order.status,
            card_number=order.withdraw_method.card_number,
            card_holder=order.withdraw_method.card_holder_name,
        )
    elif order and order.withdraw_method.method == MethodEnum.CRYPTO:
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
        "is_empty": False if order else True,
    }


@inject_getter
async def all_orders_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    **kwargs
) -> Mapping[str, str]:
    orders = await order_service.get_all_orders()
    
    return {
        "count": len(orders) if orders else 0,
        "orders": orders,
        "is_empty": orders is None or len(orders) == 0,
    }


@inject_getter
async def processing_orders_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    **kwargs
) -> Mapping[str, str]:
    orders = await order_service.get_processing_orders()
    
    return {
        "count": len(orders) if orders else 0,
        "orders": orders,
        "is_empty": orders is None or len(orders) == 0,
    }


@inject_getter
async def completed_orders_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    **kwargs
) -> Mapping[str, str]:
    orders = await order_service.get_completed_orders()
    
    return {
        "count": len(orders) if orders else 0,
        "orders": orders,
        "is_empty": orders is None or len(orders) == 0,
    }


@inject_getter
async def cancelled_orders_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    **kwargs
) -> Mapping[str, str]:
    orders = await order_service.get_cancelled_orders()
    
    return {
        "count": len(orders) if orders else 0,
        "orders": orders,
        "is_empty": orders is None or len(orders) == 0,
    }


@inject_getter
async def user_getter(
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
    **kwargs,
) -> Dict[str, UserDTO]:
    user_id = dialog_manager.dialog_data.get('search_user_id')
    user = await user_service.get_user(GetUserDTO(user_id=user_id))
    user_text = None
    if user:
        user_text = get_user_profile_text(
            user_id=user.user_id,
            commission=user.commission,
            total_withdrawn=user.total_withdrawn,
        )

    return {
        'user': user,
        'user_text': user_text,
        'is_empty': False if user else True,
    }


async def message_getter(
    dialog_manager: DialogManager,
    **kwargs,
) -> Dict[str, str]:
    message = dialog_manager.dialog_data.get('message_to_user')

    return {
        'message': message
    }


@inject_getter
async def user_orders_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    **kwargs,
) -> Dict[str, list[OrderDTO] | bool]:
    user_id = dialog_manager.dialog_data.get('search_user_id')
    orders = await order_service.list_orders(ListOrderDTO(user_id=user_id))

    return {
        'orders': orders,
        'is_empty': True if not orders else False,
    }
