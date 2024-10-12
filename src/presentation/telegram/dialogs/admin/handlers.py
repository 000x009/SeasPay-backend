from aiogram import Bot
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from src.presentation.telegram.states import (
    AdminUserOrdersSG,
    AdminOrderLookUpSG,
    OrderFulfillmentSG,
    AdminSearchSG,
)
from src.presentation.telegram.dialogs.common.injection import inject_on_click


async def selected_order(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data['order_id'] = item_id
    await dialog_manager.switch_to(AdminUserOrdersSG.ONE_ORDER)


async def selected_order_look_up(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data['order_id'] = item_id
    await dialog_manager.switch_to(AdminOrderLookUpSG.ORDER_INFO)


async def selected_user_order(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data['order_id'] = item_id
    await dialog_manager.switch_to(AdminSearchSG.USER_ORDER)


async def switch_to_fulfillment(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=OrderFulfillmentSG.ORDER_INFO,
        data={'order_id': int(dialog_manager.dialog_data.get('order_id'))},
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )


async def on_user_id(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    if not message.text.isdigit():
        await message.answer('ID пользователя введено неверно. ID должно содержать только цифры!')
    dialog_manager.dialog_data['search_user_id'] = int(data)
    await dialog_manager.switch_to(AdminSearchSG.USER)


async def on_order_id(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    if not message.text.isdigit():
        await message.answer('ID заказа введено неверно. ID должно содержать только цифры!')
        return
    dialog_manager.dialog_data['order_id'] = int(data)
    await dialog_manager.switch_to(AdminSearchSG.ORDER)


async def on_message_to_user(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    dialog_manager.dialog_data['message_to_user'] = message.text
    await dialog_manager.switch_to(AdminSearchSG.PRE_CONFIRM_MESSAGE)


@inject_on_click
async def confirm_message_sending(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    receiver_user_id = dialog_manager.dialog_data.get('search_user_id')
    message_to_user = dialog_manager.dialog_data.get('message_to_user')
    bot: Bot = dialog_manager.middleware_data.get('bot')
    await bot.send_message(
        chat_id=receiver_user_id,
        text=f"Вам пришло сообщение от администратора:\n\n<blockquote>{message_to_user}</blockquote>",
    )
    await callback_query.answer('✅ Сообщение было успешно отправлено!', show_alert=True)
    await dialog_manager.switch_to(state=AdminSearchSG.USER)
