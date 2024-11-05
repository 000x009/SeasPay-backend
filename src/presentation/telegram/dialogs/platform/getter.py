from typing import Dict, Any

from aiogram.types import ContentType

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.api.entities import MediaAttachment

from dishka.integrations.aiogram import FromDishka

from src.presentation.telegram.dialogs.common.injection import inject_getter
from src.application.services.platform import PlatformService
from src.application.dto.platform import ListPlatformDTO, GetPlatformDTO
from src.application.common.dto import Pagination
from src.infrastructure.json_text_getter import get_platform_info_text

PAGE_SIZE = 10


@inject_getter
async def platform_list_getter(
    dialog_manager: DialogManager,
    platform_service: FromDishka[PlatformService],
    **_,
) -> Dict[str, Any]:
    scroll: ManagedScroll = dialog_manager.find("scroll")
    page = await scroll.get_page()
    offset = page * PAGE_SIZE

    data = await platform_service.list_platform(ListPlatformDTO(
        pagination=Pagination(
            offset=offset,
            limit=PAGE_SIZE,
        ),
    ))

    return {
        "pages": data.total // PAGE_SIZE + bool(data.total % PAGE_SIZE),
        "platforms": data.platforms,
    }


@inject_getter
async def one_platform_getter(
    dialog_manager: DialogManager,
    platform_service: FromDishka[PlatformService],
    **_,
) -> Dict[str, Any]:
    platform_id = dialog_manager.dialog_data.get("platform_id")
    if platform_id is None:
        platform_id = dialog_manager.start_data.get("platform_id")

    platform = await platform_service.get_platform(
        GetPlatformDTO(platform_id=platform_id)
    )

    return {
        "photo": MediaAttachment(
            url=platform.image_url,
            type=ContentType.PHOTO,
        ),
        "platform": platform,
        "text": get_platform_info_text(
            name=platform.name,
            description=platform.description,
            web_place=platform.web_place,
            login_data=platform.login_data,
        )
    }


@inject_getter
async def login_data_fields_getter(
    dialog_manager: DialogManager,
    platform_service: FromDishka[PlatformService],
    **_,
) -> Dict[str, Any]:
    platform_id = dialog_manager.dialog_data.get("platform_id")
    if platform_id is None:
        platform_id = dialog_manager.start_data.get("platform_id")

    platform = await platform_service.get_platform(
        GetPlatformDTO(platform_id=platform_id)
    )
    dialog_manager.dialog_data["login_data"] = platform.login_data

    return {
        "login_data": platform.login_data,
    }
