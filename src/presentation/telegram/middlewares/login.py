from typing import Any, Awaitable, Callable, Dict, Optional, Union

from aiogram import BaseMiddleware, Router, Dispatcher
from aiogram.types import TelegramObject

from dishka import AsyncContainer, Scope

from src.application.services.user import UserService
from src.application.dto.user import GetUserDTO, CreateUserDTO


class LoginMiddleware(BaseMiddleware):
    def __init__(
        self,
        dishka_container: AsyncContainer,
        router: Optional[Union[Router, Dispatcher]] = None,
    ):
        self._dishka_container = dishka_container

        if router:
            router.message.middleware(self)
            router.callback_query.middleware(self)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]:
        async with self._dishka_container(scope=Scope.REQUEST) as request_container:
            user_service = await request_container.get(UserService)

        user_id = event.from_user.id
        user = await user_service.get_user(GetUserDTO(user_id=user_id))
        if not user:
            user = await user_service.add(CreateUserDTO(user_id=user_id))

        data["user"] = user

        return await handler(event, data)
