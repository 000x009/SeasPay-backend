from typing import Protocol
from abc import abstractmethod

from aiogram.types import ForumTopic, Message


class TelegramTopic(Protocol):
    @abstractmethod
    async def create_topic(self, name: str) -> ForumTopic:
        raise NotImplementedError
    
    @abstractmethod
    async def send_topic_message(self, thread_id: int, message: str) -> Message:
        raise NotImplementedError
    