from typing import Optional, Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatType


class ChatFilter(BaseFilter):
    def __init__(self, chat_type: Optional[ChatType] = None):
        self.chat_type = chat_type or ChatType.PRIVATE

    async def __call__(self, action: Union[Message, CallbackQuery]) -> bool:
        if isinstance(action, Message):
            return action.chat.type == self.chat_type
        elif isinstance(action, CallbackQuery):
            return action.message.chat.type == self.chat_type
