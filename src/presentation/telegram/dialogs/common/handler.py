from aiogram.types import Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput


async def message_input_fixing(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    