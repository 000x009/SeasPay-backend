from typing import Optional
import uuid

from aiogram import Bot
from aiogram.types import (
    ForumTopic,
    Message,
    BufferedInputFile,
    InlineKeyboardMarkup,
    PreparedInlineMessage,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from src.application.common.telegram import TelegramClientInterface
from src.infrastructure.config import BotSettings


class TelegramClient(TelegramClientInterface):
    def __init__(self, bot: Bot, config: BotSettings):
        self.bot = bot
        self.config = config

    async def create_topic(self, name: str) -> ForumTopic:
        return await self.bot.create_forum_topic(
            chat_id=self.config.orders_group_id,
            name=name,
        )
    
    async def send_topic_message(
        self,
        thread_id: int,
        message: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        return await self.bot.send_message(
            chat_id=self.config.orders_group_id,
            text=message,
            message_thread_id=thread_id,
            reply_markup=reply_markup,
        )
    
    async def send_message_photo(
        self,
        thread_id: int,
        photo: bytes,
        filename: Optional[str] = None,
        caption: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        buffered_photo = BufferedInputFile(photo, filename=filename)
        return await self.bot.send_photo(
            chat_id=self.config.orders_group_id,
            photo=buffered_photo,
            message_thread_id=thread_id,
            caption=caption,
            reply_markup=reply_markup,
        )

    async def save_prepared_inline_message(self, user_id: int, title: str, message_text: str) -> PreparedInlineMessage:
        return await self.bot.save_prepared_inline_message(
            user_id=user_id,
            result=InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=title,
                input_message_content=InputTextMessageContent(
                    message_text=message_text,
                    disable_web_page_preview=False,
                )
            ),
            allow_channel_chats=True,
            allow_group_chats=True,
            allow_user_chats=True,
        )

    async def edit_message(
        self,
        message_id: int,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        return await self.bot.edit_message_text(
            text=text,
            message_id=message_id,
            chat_id=self.config.orders_group_id,
            reply_markup=reply_markup,
        )

    async def send_message(self, chat_id: int, message: str) -> Message:
        return await self.bot.send_message(
            chat_id=chat_id,
            text=message,
        )

