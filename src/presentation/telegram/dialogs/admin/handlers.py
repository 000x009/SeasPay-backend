from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from src.presentation.telegram.states import AdminUserOrdersSG, AdminOrderLookUpSG, OrderFulfillmentSG


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
