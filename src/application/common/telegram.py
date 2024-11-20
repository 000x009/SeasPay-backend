from typing import Protocol, Optional
from abc import abstractmethod

from aiogram.types import ForumTopic, Message, InlineKeyboardMarkup, PreparedInlineMessage


class TelegramClientInterface(Protocol):
    @abstractmethod
    async def create_topic(self, name: str) -> ForumTopic:
        raise NotImplementedError
    
    @abstractmethod
    async def send_topic_message(
        self,
        thread_id: int,
        message: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def send_message_photo(
        self,
        thread_id: int,
        photo: bytes,
        caption: str,
        filename: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def save_prepared_inline_message(
        self,
        user_id: int,
        title: str,
        message_text: str,
    ) -> PreparedInlineMessage:
        raise NotImplementedError
