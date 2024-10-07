from typing import Optional

from aiogram import Bot
from aiogram.types import ForumTopic, Message, BufferedInputFile

from src.application.common.telegram import TelegramClientInterface
from src.infrastructure.config import BotSettings
from src.presentation.telegram.buttons.inline import get_take_order_kb_markup


class TelegramClient(TelegramClientInterface):
    def __init__(self, bot: Bot, config: BotSettings):
        self.bot = bot
        self.config = config

    async def create_topic(self, name: str) -> ForumTopic:
        return await self.bot.create_forum_topic(
            chat_id=self.config.orders_group_id,
            name=name,
        )
    
    async def send_topic_message(self, thread_id: int, message: str, order_id: int) -> Message:
        return await self.bot.send_message(
            chat_id=self.config.orders_group_id,
            text=message,
            message_thread_id=thread_id,
            reply_markup=get_take_order_kb_markup(order_id=order_id),
        )
    
    async def send_message_photo(
        self,
        thread_id: int,
        photo: bytes,
        order_id: int,
        filename: Optional[str] = None,
        caption: Optional[str] = None,
    ) -> Message:
        buffered_photo = BufferedInputFile(photo, filename=filename)
        return await self.bot.send_photo(
            chat_id=self.config.orders_group_id,
            photo=buffered_photo,
            message_thread_id=thread_id,
            caption=caption,
            reply_markup=get_take_order_kb_markup(order_id=order_id),
        )
