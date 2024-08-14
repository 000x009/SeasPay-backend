from src.infrastructure.dal import UserDAL
from src.application.dto import UserDTO


class UserService():
    def __init__(self, user_dal: UserDAL) -> None:
        self.__user_dal = user_dal

    async def add(self, values: UserDTO) -> None:
        await self.__user_dal.insert(values=values)
