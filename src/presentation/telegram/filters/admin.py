from aiogram.filters import BaseFilter
from aiogram.types import Message


class AdminFilter(BaseFilter):
    def __init__(self) -> None:
        self._admins = (5297779345,)

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self._admins
