from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from src.presentation.telegram.states import AdminUserOrdersSG


async def selected_order(
    callback_query: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data['order_id'] = item_id
    await dialog_manager.switch_to(AdminUserOrdersSG.ONE_ORDER)
