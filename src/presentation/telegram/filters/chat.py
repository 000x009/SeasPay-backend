from typing import Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums import ChatType


class ChatFilter(BaseFilter):
    def __init__(self, chat_type: Optional[ChatType] = None):
        self.chat_type = chat_type or ChatType.PRIVATE

    async def __call__(self, message: Message) -> bool:
        return message.chat.type == self.chat_type
