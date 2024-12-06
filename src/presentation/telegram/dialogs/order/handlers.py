import uuid
from decimal import Decimal
import logging

from aiogram import Bot
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput
from dishka.integrations.aiogram import FromDishka

from src.application.services.order import OrderService
from src.application.dto.order import (
    FulfillWithdrawOrderDTO,
    FulfillTransferOrderDTO,
    GetOrderDTO,
    CancelOrderDTO,
    FulfillDigitalProductOrderDTO,
)
from src.presentation.telegram.dialogs.common.injection import inject_on_click
from src.presentation.telegram.states.admin_order import OrderFulfillmentSG
from src.infrastructure.config import load_bot_settings
from src.infrastructure.json_text_getter import get_paypal_order_text
from src.infrastructure.json_text_getter import (
    get_order_successfully_fulfilled_text,
    get_transfer_successfully_fulfilled_text,
    get_digital_product_successfully_fulfilled_text,
)
from src.domain.value_objects.order import OrderTypeEnum
from src.application.services.transfer_details import TransferDetailsService
from src.application.services.withdraw_details import WithdrawService
from src.application.dto.transfer_details import CalculateTransferCommissionDTO
from src.application.dto.withdraw_details import CalculateWithdrawCommissionDTO
from src.presentation.telegram.buttons import inline


async def calculate_commission(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(OrderFulfillmentSG.CALCULATE_COMMISSION)


@inject_on_click
async def on_wrote_paypal_received_amount(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
    order_service: FromDishka[OrderService],
    transfer_service: FromDishka[TransferDetailsService],
    withdraw_service: FromDishka[WithdrawService],
) -> None:
    order_id = dialog_manager.start_data.get("order_id")
    order = await order_service.get(GetOrderDTO(order_id=uuid.UUID(order_id)))
    commission = None
    if order.type == OrderTypeEnum.TRANSFER:
        commission = await transfer_service.calculate_commission(CalculateTransferCommissionDTO(
            order_id=order.id,
            payment_system_received_amount=Decimal(data),
        ))
    elif order.type == OrderTypeEnum.WITHDRAW:
        commission = await withdraw_service.calculate_commission(CalculateWithdrawCommissionDTO(
            order_id=order.id,
            payment_system_received_amount=Decimal(data),
        ))

    dialog_manager.dialog_data["received_amount"] = float(data)
    dialog_manager.dialog_data["user_must_receive"] = float(commission.recipient_must_receive)
    await dialog_manager.switch_to(OrderFulfillmentSG.ORDER_INFO)


async def attach_receipt(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(OrderFulfillmentSG.ATTACH_RECEIPT)


async def on_attach_receipt(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
) -> None:
    if message.photo:
        dialog_manager.dialog_data["payment_receipt_id"] = message.photo[-1].file_id
        await message.delete()
        await dialog_manager.switch_to(OrderFulfillmentSG.ORDER_INFO)
    else:
        await message.answer("Пожалуйста, отправьте фото")


async def pre_confirm_fulfillment(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(OrderFulfillmentSG.PRE_CONFIRM)


@inject_on_click
async def confirm_fulfillment(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService]
) -> None:
    bot: Bot = dialog_manager.middleware_data.get("bot")
    order_id = dialog_manager.start_data.get("order_id")
    user_received_amount = dialog_manager.dialog_data.get("user_received_amount")
    received_amount = dialog_manager.dialog_data.get("received_amount")
    order_type = dialog_manager.dialog_data.get("order_type")
    bot_settings = load_bot_settings()

    try:
        order = None
        if order_type == OrderTypeEnum.WITHDRAW:
            order = await order_service.fulfill_withdraw_order(FulfillWithdrawOrderDTO(
                order_id=order_id,
                payment_system_received_amount=Decimal(received_amount),
                user_received_amount=Decimal(user_received_amount),
            ))
        elif order_type == OrderTypeEnum.TRANSFER:
            order = await order_service.fulfill_transfer_order(FulfillTransferOrderDTO(order_id=order_id))
        elif order_type == OrderTypeEnum.DIGITAL_PRODUCT:
            order = await order_service.fulfill_digital_product_order(FulfillDigitalProductOrderDTO(
                order_id=order_id,
            ))
        await bot.edit_message_text(
            chat_id=bot_settings.orders_group_id,
            message_id=order.telegram_message_id,
            text=get_paypal_order_text(
                order_id=order.id,
                user_id=order.user_id,
                created_at=order.created_at,
                status=order.status,
                order_type=order.type,
            ),
        )
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="✅ Заказ был успешно выполнен!"
        )
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id
        )

        order = await order_service.get(GetOrderDTO(order_id=order_id))
        successfully_fulfilled_text = None
        if order.type == OrderTypeEnum.TRANSFER:
            successfully_fulfilled_text = get_transfer_successfully_fulfilled_text(order_id=order_id)
        elif order.type == OrderTypeEnum.DIGITAL_PRODUCT:
            successfully_fulfilled_text = get_digital_product_successfully_fulfilled_text(order_id=order_id)
        elif order.type == OrderTypeEnum.WITHDRAW:
            successfully_fulfilled_text = get_order_successfully_fulfilled_text(amount=received_amount)

        await bot.send_message(
            chat_id=order.user_id,
            text=successfully_fulfilled_text,
            reply_markup=inline.post_feedback_kb_markup,
        )
    except Exception as e:
        logging.error(f"Error sending message: {e}")
    finally:
        await dialog_manager.done()


@inject_on_click
async def cancel_order_handler(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    order_service: FromDishka[OrderService],
) -> None:
    bot = dialog_manager.middleware_data.get("bot")
    order_id = dialog_manager.start_data.get("order_id")
    bot_settings = load_bot_settings()

    try:
        order = await order_service.cancel_order(CancelOrderDTO(order_id=order_id))
        await bot.edit_message_text(
            chat_id=bot_settings.orders_group_id,
            message_id=order.telegram_message_id,
            text=get_paypal_order_text(
                order_id=order.id,
                user_id=order.user_id,
                created_at=order.created_at,
                status=order.status,
                order_type=order.type,
            ),
        )
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="✅ Заказ был успешно отменен!"
        )
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id
        )
        await bot.send_message(
            chat_id=order.user_id,
            text=f"Здравствуйте, к сожалению ваш запрос на вывод средств <code>№{order.id}</code> был отменен по причине\n: <blockquote>{dialog_manager.dialog_data.get('reason')}</blockquote>"
        )
    except Exception as e:
        logging.error(f"Error canceling order: {e}")
    finally:
        await dialog_manager.done()


async def on_reason_cancel_order(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data["reason"] = message.text
    await dialog_manager.switch_to(OrderFulfillmentSG.CANCEL_ORDER)


async def on_user_received_amount(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
) -> None:
    if message.text.isdigit():
        dialog_manager.dialog_data["user_received_amount"] = message.text
        await dialog_manager.switch_to(OrderFulfillmentSG.ORDER_INFO)
        await message.answer("Сумма была успешно установлена!")
    else:
        await message.answer("Пожалуйста, введите число")
