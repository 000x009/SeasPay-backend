import uuid
from typing import Dict
from decimal import Decimal

from aiogram.types import ContentType

from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from dishka.integrations.aiogram import FromDishka

from src.application.dto.user import GetUserDTO
from src.application.services.order import OrderService
from src.application.services.user import UserService
from src.application.services.withdraw_details import WithdrawService
from src.application.dto.withdraw_details import GetWithdrawDetailsDTO
from src.application.services.transfer_details import TransferDetailsService
from src.application.dto.transfer_details import GetTransferDetailsDTO
from src.application.dto.order import GetOrderDTO, OrderDTO
from src.presentation.telegram.dialogs.common.injection import inject_getter
from src.domain.value_objects.withdraw_method import MethodEnum
from src.domain.value_objects.order import OrderTypeEnum
from src.infrastructure.json_text_getter import (
    get_paypal_order_text,
    get_withdraw_card_text,
    get_withdraw_crypto_text,
    get_transfer_text,
    get_digital_product_details_text,
)
from src.application.services.digital_product_details import DigitalProductDetailsService
from src.application.dto.digital_product_details import GetDigitalProductDetailsDTO


@inject_getter
async def order_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    user_service: FromDishka[UserService],
    **_,
) -> Dict[str, OrderDTO]:
    order_id = uuid.UUID(dialog_manager.start_data.get("order_id"))
    user_received_amount = dialog_manager.dialog_data.get("user_received_amount")
    order = await order_service.get(GetOrderDTO(order_id=order_id))
    customer = await user_service.get_user(GetUserDTO(user_id=order.user_id))
    dialog_manager.dialog_data["order_type"] = order.type

    payment_receipt_id = dialog_manager.dialog_data.get("payment_receipt_id")
    payment_receipt = None
    if payment_receipt_id:
        payment_receipt = MediaAttachment(
            file_id=MediaId(file_id=payment_receipt_id),
            type=ContentType.PHOTO,
        )

    return {
        "order": order,
        "order_type": order.type,
        "customer": customer,
        "payment_receipt": payment_receipt if payment_receipt else None,
        "user_received_amount": user_received_amount,
    }


@inject_getter
async def order_text_getter(
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
    withdraw_service: FromDishka[WithdrawService],
    transfer_details_service: FromDishka[TransferDetailsService],
    digital_product_service: FromDishka[DigitalProductDetailsService],
    **_,
) -> Dict[str, str]:
    order_id = uuid.UUID(dialog_manager.start_data.get("order_id"))
    order = await order_service.get(GetOrderDTO(order_id=order_id))
    details_text = ""

    if order.type == OrderTypeEnum.WITHDRAW:
        db_details = await withdraw_service.get_withdraw_method(GetWithdrawDetailsDTO(order_id=order.id))
        user_must_receive = dialog_manager.dialog_data.get("user_must_receive")
        if user_must_receive:
            received_amount = dialog_manager.dialog_data.get("received_amount")
            if db_details.method == MethodEnum.CARD:
                details_text = get_withdraw_card_text(
                    card_number=db_details.card_number,
                    card_holder=db_details.card_holder_name,
                    user_must_receive=round(user_must_receive, 2),
                    commission=db_details.commission,
                    profit=round(received_amount - user_must_receive, 2),
                )
            elif db_details.method == MethodEnum.CRYPTO:
                details_text = get_withdraw_crypto_text(
                    address=db_details.crypto_address,
                    network=db_details.crypto_network,
                    user_must_receive=round(user_must_receive, 2),
                    commission=db_details.commission,
                    profit=round(Decimal(received_amount) - user_must_receive, 2),
                )
    elif order.type == OrderTypeEnum.TRANSFER:
        db_details = await transfer_details_service.get_details(GetTransferDetailsDTO(order_id=order.id))
        details_text = get_transfer_text(
            receiver_email=db_details.receiver_email,
            amount=db_details.amount,
            commission=db_details.commission,
        )
    elif order.type == OrderTypeEnum.DIGITAL_PRODUCT:
        db_details = await digital_product_service.get(GetDigitalProductDetailsDTO(order_id=order.id))
        details_text = get_digital_product_details_text(
            product_purchase_url=db_details.purchase_url,
            login_data=db_details.login_data,
        )

    return {
        "details_text": details_text,
        "order_text": get_paypal_order_text(
            order_id=order.id,
            user_id=order.user_id,
            created_at=order.created_at,
            status=order.status,
            order_type=order.type,
        ),
    }


async def order_cancel_getter(
    dialog_manager: DialogManager,
    **_,
) -> Dict[str, str]:
    return {
        "reason": dialog_manager.dialog_data.get("reason"),
    }
