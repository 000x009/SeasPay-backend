from typing import Protocol, Optional
from abc import abstractmethod
from uuid import UUID

from aiogram.types import ForumTopic, Message, InlineKeyboardMarkup


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
