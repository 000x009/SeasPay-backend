import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ChatType

from dishka import FromDishka

from src.presentation.telegram.buttons.inline import get_start_kb_markup
from src.infrastructure.config import load_bot_settings
from src.presentation.telegram.filters import ChatFilter
from src.application.services.user import UserService
from src.application.dto.user import GetUserDTO, CreateUserDTO


router = Router()


@router.message(CommandStart(), ChatFilter(chat_type=ChatType.PRIVATE))
async def start_handler(
    message: Message,
    bot: Bot,
    user_service: FromDishka[UserService],
) -> None:
    bot_config = load_bot_settings()
    await bot.send_message(
        chat_id=message.from_user.id,
        text='OverseasPay!',
        reply_markup=get_start_kb_markup(config=bot_config),
    )

    try:
        user_id = message.from_user.id
        user = await user_service.get_user(GetUserDTO(user_id=user_id))
        if not user:
            await user_service.add(CreateUserDTO(user_id=user_id))
    except Exception as e:
        print(e)
