from typing import Optional

from src.infrastructure.dal import UserDAL
from src.application.dto.user import CreateUserDTO, GetUserDTO, UserDTO


class UserService:
    def __init__(self, user_dal: UserDAL) -> None:
        self._user_dal = user_dal

    async def add(self, data: CreateUserDTO) -> None:
        await self._user_dal.insert(values=data)

    async def get_user(self, data: GetUserDTO) -> Optional[UserDTO, None]:
        await self._user_dal.get_one(values=data)
