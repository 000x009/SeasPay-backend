from aiogram.filters import BaseFilter
from aiogram.types import Message


ADMIN_LIST = (5297779345, 6384960822, 563603481, 563603481)


class AdminFilter(BaseFilter):
    def __init__(self) -> None:
        self._admins = ADMIN_LIST

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self._admins
