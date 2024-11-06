from typing import Any, Dict

from dishka import FromDishka

from aiogram.types import ContentType

from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.common import ManagedScroll

from src.presentation.telegram.dialogs.common.injection import inject_getter
from src.application.services.platform_product import PlatformProductService
from src.application.dto.platform_product import ListPlatformProductDTO, GetPlatformProductDTO
from src.application.common.dto import Pagination
from src.infrastructure.json_text_getter import get_platform_product_text


PAGE_SIZE = 10


@inject_getter
async def platform_product_getter(
    dialog_manager: DialogManager,
    platform_product_service: FromDishka[PlatformProductService],
    **_,
) -> Dict[str, Any]:
    scroll: ManagedScroll = dialog_manager.find("scroll")
    page = await scroll.get_page()
    offset = page * PAGE_SIZE

    platform_id = dialog_manager.start_data.get("platform_id")
    data = await platform_product_service.list_platform_product(ListPlatformProductDTO(
        platform_id=platform_id,
        pagination=Pagination(
            limit=PAGE_SIZE,
            offset=offset,
        ),
    ))

    return {
        "pages": data.total // PAGE_SIZE + bool(data.total % PAGE_SIZE),
        "products": data.products,
    }


@inject_getter
async def get_platform_product_getter(
    dialog_manager: DialogManager,
    platform_product_service: FromDishka[PlatformProductService],
    **_,
) -> Dict[str, Any]:
    product_id = dialog_manager.dialog_data.get("product_id")
    data = await platform_product_service.get_platform_product(GetPlatformProductDTO(id=product_id))

    return {
        "text": get_platform_product_text(
            product_id=data.id,
            name=data.name,
            price=data.price,
            instruction=data.instruction,
        ),
        "product": data,
        "photo": MediaAttachment(
            url=data.image_url,
            type=ContentType.PHOTO,
        ),
    }
