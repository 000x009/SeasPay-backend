from typing import Optional

from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData

from fastapi import Request

from src.infrastructure.config import load_settings
from src.domain.exceptions.user import NotAuthorizedError


async def user_init_data_provider(request: Request) -> Optional[WebAppInitData]:
    try:
        auth_string = request.headers.get('Authorization')
        if auth_string:
            settings = load_settings()
            return safe_parse_webapp_init_data(settings.bot.bot_token, auth_string)
        else:
            raise NotAuthorizedError('Not authorized.')
    except ValueError:
        raise NotAuthorizedError('Wrong web app init data.')
