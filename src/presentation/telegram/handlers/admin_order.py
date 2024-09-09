from aiogram import Router, Bot, F
from aiogram.enums import ChatType
from aiogram.types import CallbackQuery

from src.presentation.telegram.filters import AdminFilter, ChatFilter


router = Router()


@router.message(
    F.data.startswith('confirm_order'),
    AdminFilter(),
    ChatFilter(chat_type=ChatType.SUPERGROUP),
)
async def confirm_order_handler(
    callback: CallbackQuery,
    bot: Bot,
) -> None:
    order_id = callback.data.split(':')[1]
    pass
