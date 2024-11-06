from decimal import Decimal

from aiogram import Bot
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from dishka import FromDishka

from src.presentation.telegram.states.platform_products import PlatformProductManagementSG
from src.presentation.telegram.states.platform import PlatformManagementSG
from src.presentation.telegram.dialogs.common.injection import inject_on_click
from src.application.services.platform_product import PlatformProductService
from src.application.dto.platform_product import GetPlatformProductDTO, DeletePlatformProductDTO, UpdatePlatformProductDTO, AddPlatformProductDTO
from src.application.dto.cloud import UploadObjectDTO
from src.application.services.cloud import CloudService
from src.infrastructure.config import app_settings


async def on_selected_product(
    event: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    product_id: int,
) -> None:
    dialog_manager.dialog_data["product_id"] = product_id
    await dialog_manager.switch_to(
        state=PlatformProductManagementSG.PRODUCT,
    )


async def back_to_platform(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=PlatformManagementSG.PLATFORM,
        data=dialog_manager.start_data,
        show_mode=ShowMode.EDIT,
    )

@inject_on_click
async def delete_platform_product(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    platform_product_service: FromDishka[PlatformProductService],
) -> None:
    await platform_product_service.delete_platform_product(
        DeletePlatformProductDTO(
            id=dialog_manager.dialog_data["product_id"],
        )
    )
    await dialog_manager.switch_to(
        state=PlatformProductManagementSG.PRODUCT_LIST,
    )


@inject_on_click
async def on_edit_platform_product_name(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
    platform_product_service: FromDishka[PlatformProductService],
) -> None:
    product_id = dialog_manager.dialog_data["product_id"]
    product = await platform_product_service.get_platform_product(
        GetPlatformProductDTO(
            id=product_id,
        )
    )
    await platform_product_service.update_platform_product(
        UpdatePlatformProductDTO(
            platform_id=product.platform_id,
            product_id=product_id,
            name=event.text,
            instruction=product.instruction,
            purchase_url=product.purchase_url,
            image_url=product.image_url,
            price=product.price,
        )
    )
    await dialog_manager.switch_to(
        state=PlatformProductManagementSG.PRODUCT,
    )



@inject_on_click
async def on_edit_platform_product_instruction(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
    platform_product_service: FromDishka[PlatformProductService],
) -> None:
    product_id = dialog_manager.dialog_data["product_id"]
    product = await platform_product_service.get_platform_product(
        GetPlatformProductDTO(
            id=product_id,
        )
    )
    await platform_product_service.update_platform_product(
        UpdatePlatformProductDTO(
            platform_id=product.platform_id,
            product_id=product_id,
            instruction=data,
            name=product.name,
            purchase_url=product.purchase_url,
            image_url=product.image_url,
            price=product.price,
        )
    )
    await dialog_manager.switch_to(
        state=PlatformProductManagementSG.PRODUCT,
    )


@inject_on_click
async def on_edit_platform_product_purchase_url(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
    platform_product_service: FromDishka[PlatformProductService],
) -> None:
    product_id = dialog_manager.dialog_data["product_id"]
    product = await platform_product_service.get_platform_product(
        GetPlatformProductDTO(
            id=product_id,
        )
    )
    await platform_product_service.update_platform_product(
        UpdatePlatformProductDTO(
            product_id=product_id,
            purchase_url=data,
            platform_id=product.platform_id,
            name=product.name,
            instruction=product.instruction,
            image_url=product.image_url,
            price=product.price,
        )
    )
    await dialog_manager.switch_to(
        state=PlatformProductManagementSG.PRODUCT,
    )



@inject_on_click
async def on_edit_platform_product_price(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    platform_product_service: FromDishka[PlatformProductService],
) -> None:
    if not event.text.isdigit():
        await event.answer("Цена должна быть числом!")
    else:
        product_id = dialog_manager.dialog_data["product_id"]
        product = await platform_product_service.get_platform_product(
            GetPlatformProductDTO(
                id=product_id,
            )
        )
        await platform_product_service.update_platform_product(
            UpdatePlatformProductDTO(
                platform_id=product.platform_id,
                product_id=product_id,
                price=Decimal(event.text),
                name=product.name,
                instruction=product.instruction,
                purchase_url=product.purchase_url,
                image_url=product.image_url,
            )
        )
        await dialog_manager.switch_to(
            state=PlatformProductManagementSG.PRODUCT,
        )


@inject_on_click
async def on_edit_platform_product_image(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    cloud_storage: FromDishka[CloudService],
    platform_product_service: FromDishka[PlatformProductService],
) -> None:
    bot: Bot = dialog_manager.middleware_data.get("bot")
    file = await bot.get_file(event.photo[-1].file_id)
    photo = await bot.download_file(file.file_path)
    image = cloud_storage.upload_object(UploadObjectDTO(
        bucket=app_settings.cloud_settings.products_bucket_name,
        filename=f"{event.photo[-1].file_id}.jpg",
        file=photo,
    ))
    
    product = await platform_product_service.get_platform_product(
        GetPlatformProductDTO(
            id=dialog_manager.dialog_data["product_id"],
        )
    )
    await platform_product_service.update_platform_product(
        UpdatePlatformProductDTO(
            platform_id=product.platform_id,
            product_id=dialog_manager.dialog_data["product_id"],
            image_url=image.url,
            name=product.name,
            instruction=product.instruction,
            purchase_url=product.purchase_url,
            price=product.price,
        )
    )
    await dialog_manager.switch_to(
        state=PlatformProductManagementSG.PRODUCT,
    )


@inject_on_click
async def on_new_platform_product_name(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    dialog_manager.dialog_data["product_name"] = data
    await dialog_manager.switch_to(
        state=PlatformProductManagementSG.ADD_PRODUCT_INSTRUCTION,
    )


@inject_on_click
async def on_new_platform_product_instruction(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    dialog_manager.dialog_data["product_instruction"] = data
    await dialog_manager.switch_to(
        state=PlatformProductManagementSG.ADD_PRODUCT_PURCHASE_URL,
    )


@inject_on_click
async def on_new_platform_product_purchase_url(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    dialog_manager.dialog_data["product_purchase_url"] = data
    await dialog_manager.switch_to(
        state=PlatformProductManagementSG.ADD_PRODUCT_PRICE,
    )


@inject_on_click
async def on_new_platform_product_price(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
) -> None:
    if not data.isdigit():
        await event.answer("Цена должна быть числом!")
    else:
        dialog_manager.dialog_data["product_price"] = data
        await dialog_manager.switch_to(
            state=PlatformProductManagementSG.ADD_PRODUCT_IMAGE,
        )


@inject_on_click
async def on_new_platform_product_image(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    cloud_storage: FromDishka[CloudService],
    platform_product_service: FromDishka[PlatformProductService],
) -> None:
    bot: Bot = dialog_manager.middleware_data.get("bot")
    file = await bot.get_file(event.photo[-1].file_id)
    photo = await bot.download_file(file.file_path)
    image = cloud_storage.upload_object(UploadObjectDTO(
        bucket=app_settings.cloud_settings.products_bucket_name,
        filename=f"{event.photo[-1].file_id}.jpg",
        file=photo,
    ))
    product = await platform_product_service.add_platform_product(
        AddPlatformProductDTO(
            name=dialog_manager.dialog_data["product_name"],
            instruction=dialog_manager.dialog_data["product_instruction"],
            purchase_url=dialog_manager.dialog_data["product_purchase_url"],
            price=Decimal(dialog_manager.dialog_data["product_price"]),
            image_url=image.url,
            platform_id=dialog_manager.start_data["platform_id"],
        )
    )
    dialog_manager.dialog_data["product_id"] = product.id
    
    await dialog_manager.switch_to(
        state=PlatformProductManagementSG.PRODUCT_LIST,
    )
