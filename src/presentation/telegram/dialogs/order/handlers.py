from decimal import Decimal
import logging

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput
from dishka.integrations.aiogram import FromDishka

from src.application.services.order import OrderService
from src.application.dto.order import CalculateCommissionDTO, FulfillOrderDTO, GetOrderDTO, CancelOrderDTO
from src.presentation.telegram.dialogs.common.injection import inject_on_click
from src.presentation.telegram.states.admin_order import OrderFulfillmentSG
from src.infrastructure.config import load_bot_settings
from src.infrastructure.json_text_getter import get_paypal_withdraw_order_text


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
    value: str,
    order_service: FromDishka[OrderService]
) -> None:
    order_id = dialog_manager.start_data.get("order_id")
    commission = await order_service.calculate_commission(
        CalculateCommissionDTO(
            order_id=order_id,
            paypal_received_amount=Decimal(value),
        )
    )
    dialog_manager.dialog_data["received_amount"] = float(value)
    dialog_manager.dialog_data["user_must_receive"] = float(commission.user_must_receive)
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
    bot = dialog_manager.middleware_data.get("bot")
    order_id = dialog_manager.start_data.get("order_id")
    user_received_amount = dialog_manager.dialog_data.get("user_received_amount")
    bot_settings = load_bot_settings()

    try:
        order = await order_service.fulfill_order(FulfillOrderDTO(
            order_id=order_id,
            paypal_received_amount=Decimal(dialog_manager.dialog_data.get("received_amount")),
            user_received_amount=Decimal(user_received_amount)
        ))
        await bot.edit_message_caption(
            chat_id=bot_settings.orders_group_id,
            message_id=order.telegram_message_id,
            caption=get_paypal_withdraw_order_text(
                order_id=order.id,
                user_id=order.user_id,
                created_at=order.created_at,
                status=order.status.value,
                commission=order.commission,
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
        await bot.send_message(
            chat_id=order.user_id,
            text=f"Ваш запрос <code>№{order.id}</code> на вывод средств успешно был выполнен!"
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
        await bot.edit_message_caption(
            chat_id=bot_settings.orders_group_id,
            message_id=order.telegram_message_id,
            caption=get_paypal_withdraw_order_text(
                order_id=order.id,
                user_id=order.user_id,
                created_at=order.created_at,
                status=order.status.value,
                commission=order.commission,
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
