from typing import Protocol, Optional
from abc import abstractmethod

from aiogram.types import ForumTopic, Message


class TelegramClientInterface(Protocol):
    @abstractmethod
    async def create_topic(self, name: str) -> ForumTopic:
        raise NotImplementedError
    
    @abstractmethod
    async def send_topic_message(self, thread_id: int, message: str) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def send_message_photo(
        self,
        thread_id: int,
        photo: bytes,
        order_id: int,
        caption: str,
        filename: Optional[str] = None,
    ) -> Message:
        raise NotImplementedError
