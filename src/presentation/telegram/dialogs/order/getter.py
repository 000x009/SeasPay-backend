from typing import Mapping
from decimal import Decimal

from aiogram.types import ContentType

from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from dishka.integrations.aiogram import FromDishka

from src.application.dto.user import GetUserDTO
from src.application.services.order import OrderService
from src.application.services.user import UserService
from src.application.dto.order import GetOrderDTO, OrderDTO
from src.presentation.telegram.dialogs.common.injection import inject_getter
from src.domain.value_objects.withdraw_method import MethodEnum
from src.infrastructure.json_text_getter import (
    get_paypal_withdraw_order_text,
    get_withdraw_card_text,
    get_withdraw_crypto_text,
)


@inject_getter
async def order_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    user_service: FromDishka[UserService],
    **kwargs
) -> Mapping[str, OrderDTO]:
    order_id = dialog_manager.start_data.get("order_id")
    user_received_amount = dialog_manager.dialog_data.get("user_received_amount")
    order = await order_service.get(GetOrderDTO(order_id=order_id))
    customer = await user_service.get_user(GetUserDTO(user_id=order.user_id))

    withdraw_method_text = ""
    user_must_receive = dialog_manager.dialog_data.get("user_must_receive")
    if user_must_receive:
        received_amount = dialog_manager.dialog_data.get("received_amount")
        if order.withdraw_method.method == MethodEnum.CARD:
            withdraw_method_text = get_withdraw_card_text(
                card_number=order.withdraw_method.card_number,
                card_holder=order.withdraw_method.card_holder_name,
                user_must_receive=round(user_must_receive, 2),
                commission=order.commission,
                profit=round(received_amount - user_must_receive, 2),
            )
        elif order.withdraw_method.method == MethodEnum.CRYPTO:
            withdraw_method_text = get_withdraw_crypto_text(
                address=order.withdraw_method.crypto_address,
                network=order.withdraw_method.crypto_network,
                user_must_receive=round(user_must_receive, 2),
                commission=order.commission,
                profit=round(Decimal(received_amount) - user_must_receive, 2),
            )

    payment_receipt_id = dialog_manager.dialog_data.get("payment_receipt_id")
    payment_receipt = None
    if payment_receipt_id:
        payment_receipt = MediaAttachment(
            file_id=MediaId(file_id=payment_receipt_id),
            type=ContentType.PHOTO,
        )

    return {
        "order": order,
        "customer": customer,
        "order_text": get_paypal_withdraw_order_text(
            order_id=order.id,
            user_id=order.user_id,
            created_at=order.created_at,
            status=order.status.value,
            commission=order.commission,
        ),
        "withdraw_method_text": withdraw_method_text,
        "payment_receipt": payment_receipt if payment_receipt else None,
        "user_received_amount": user_received_amount,
    }


async def order_cancel_getter(
    dialog_manager: DialogManager,
    **kwargs
) -> Mapping[str, str]:
    return {
        "reason": dialog_manager.dialog_data.get("reason"),
    }
