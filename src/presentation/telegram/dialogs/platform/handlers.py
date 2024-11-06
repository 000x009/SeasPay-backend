from aiogram import Bot
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from dishka.integrations.aiogram import FromDishka

from src.presentation.telegram.states.platform import PlatformManagementSG
from src.presentation.telegram.states.platform_products import PlatformProductManagementSG
from src.presentation.telegram.dialogs.common.injection import inject_on_click
from src.application.services.platform import PlatformService
from src.application.services.cloud import CloudService
from src.application.dto.cloud import UploadObjectDTO
from src.application.dto.platform import DeletePlatformDTO, UpdatePlatformDTO, GetPlatformDTO, CreatePlatformDTO
from src.infrastructure.config import app_settings


EMAIL_PASSWORD_LOGIN_DATA = ['Почта', 'Пароль']


async def on_selected_platform(
    event: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    platform_id: int,
) -> None:
    dialog_manager.dialog_data["platform_id"] = platform_id
    await dialog_manager.switch_to(
        state=PlatformManagementSG.PLATFORM,
    )


@inject_on_click
async def delete_platform(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    platform_service: FromDishka[PlatformService],
) -> None:
    platform_id = dialog_manager.dialog_data["platform_id"]
    await platform_service.delete_platform(
        DeletePlatformDTO(platform_id=platform_id)
    )
    await dialog_manager.switch_to(state=PlatformManagementSG.PLATFORM_LIST)


@inject_on_click
async def on_edit_platform_name(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
    platform_service: FromDishka[PlatformService],
) -> None:
    platform_id = dialog_manager.dialog_data.get("platform_id")
    platform = await platform_service.get_platform(
        GetPlatformDTO(platform_id=platform_id)
    )
    await platform_service.update_platform(
        UpdatePlatformDTO(
            platform_id=dialog_manager.dialog_data["platform_id"],
            name=value,
            image_url=platform.image_url,
            web_place=platform.web_place,
            description=platform.description,
            login_data=platform.login_data,
        )
    )
    await dialog_manager.switch_to(state=PlatformManagementSG.PLATFORM_INFO)


@inject_on_click
async def on_edit_platform_description(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
    platform_service: FromDishka[PlatformService],
) -> None:
    platform_id = dialog_manager.dialog_data.get("platform_id")
    platform = await platform_service.get_platform(
        GetPlatformDTO(platform_id=platform_id)
    )
    await platform_service.update_platform(
        UpdatePlatformDTO(
            platform_id=dialog_manager.dialog_data["platform_id"],
            name=platform.name,
            image_url=platform.image_url,
            web_place=platform.web_place,
            description=value,
            login_data=platform.login_data,
        )
    )
    await dialog_manager.switch_to(state=PlatformManagementSG.PLATFORM_INFO)


@inject_on_click
async def on_edit_platform_web_place(
    event: Message,
    widget: ManagedTextInput[int],
    dialog_manager: DialogManager,
    value: int,
    platform_service: FromDishka[PlatformService],
) -> None:
    platform_id = dialog_manager.dialog_data.get("platform_id")
    platform = await platform_service.get_platform(
        GetPlatformDTO(platform_id=platform_id)
    )
    await platform_service.update_platform(
        UpdatePlatformDTO(
            platform_id=dialog_manager.dialog_data["platform_id"],
            name=platform.name,
            image_url=platform.image_url,
            web_place=value,
            description=platform.description,
            login_data=platform.login_data,
        )
    )
    await dialog_manager.switch_to(state=PlatformManagementSG.PLATFORM_INFO)


@inject_on_click
async def on_edit_platform_image(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    platform_service: FromDishka[PlatformService],
    cloud_storage: FromDishka[CloudService],
) -> None:
    platform_id = dialog_manager.dialog_data.get("platform_id")
    platform = await platform_service.get_platform(
        GetPlatformDTO(platform_id=platform_id)
    )
    bot: Bot = dialog_manager.middleware_data.get("bot")
    file = await bot.get_file(event.photo[-1].file_id)
    photo = await bot.download_file(file.file_path)
    image = cloud_storage.upload_object(UploadObjectDTO(
        bucket=app_settings.cloud_settings.platforms_bucket_name,
        filename=f"{event.photo[-1].file_id}.jpg",
        file=photo,
    ))

    await platform_service.update_platform(
        UpdatePlatformDTO(
            platform_id=dialog_manager.dialog_data["platform_id"],
            name=platform.name,
            image_url=image.url,
            web_place=platform.web_place,
            description=platform.description,
            login_data=platform.login_data,
        )
    )
    await dialog_manager.switch_to(state=PlatformManagementSG.PLATFORM_INFO)


@inject_on_click
async def remove_login_field(
    event: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    login_field: str,
    platform_service: FromDishka[PlatformService],
) -> None:
    login_data = dialog_manager.dialog_data["login_data"]
    login_data.remove(login_field)
    dialog_manager.dialog_data["login_data"] = login_data
    platform = await platform_service.get_platform(GetPlatformDTO(
            platform_id=dialog_manager.dialog_data.get("platform_id"),
        )
    )
    await platform_service.update_platform(
        UpdatePlatformDTO(
            platform_id=platform.platform_id,
            name=platform.name,
            image_url=platform.image_url,
            web_place=platform.web_place,
            description=platform.description,
            login_data=login_data,
        )
    )
    await dialog_manager.switch_to(state=PlatformManagementSG.EDIT_LOGIN_DATA)


@inject_on_click
async def add_login_field(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    login_field: str,
    platform_service: FromDishka[PlatformService],
) -> None:
    login_data = dialog_manager.dialog_data["login_data"]
    login_data.append(login_field)
    dialog_manager.dialog_data["login_data"] = login_data
    platform = await platform_service.get_platform(GetPlatformDTO(
            platform_id=dialog_manager.dialog_data.get("platform_id"),
        )
    )
    await platform_service.update_platform(
        UpdatePlatformDTO(
            platform_id=platform.platform_id,
            name=platform.name,
            image_url=platform.image_url,
            web_place=platform.web_place,
            description=platform.description,
            login_data=login_data,
        )
    )
    await dialog_manager.switch_to(state=PlatformManagementSG.EDIT_LOGIN_DATA)


async def on_new_platform_name(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
) -> None:
    dialog_manager.dialog_data["name"] = value
    await dialog_manager.switch_to(state=PlatformManagementSG.ADD_PLATFORM_DESCRIPTION)


async def on_new_platform_description(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
) -> None:
    dialog_manager.dialog_data["description"] = value
    await dialog_manager.switch_to(state=PlatformManagementSG.ADD_PLATFORM_LOGIN_DATA)


async def on_new_platform_login_data(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    value: str,
) -> None:
    login_data = list(map(str.strip, value.split(",")))
    dialog_manager.dialog_data["login_data"] = login_data
    await dialog_manager.switch_to(state=PlatformManagementSG.ADD_PLATFORM_IMAGE)


async def email_password_login_data(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data["login_data"] = EMAIL_PASSWORD_LOGIN_DATA
    await dialog_manager.switch_to(state=PlatformManagementSG.ADD_PLATFORM_IMAGE)


@inject_on_click
async def on_new_platform_image(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    cloud_storage: FromDishka[CloudService],
    platform_service: FromDishka[PlatformService],
) -> None:
    bot: Bot = dialog_manager.middleware_data.get("bot")
    file = await bot.get_file(event.photo[-1].file_id)
    photo = await bot.download_file(file.file_path)
    image = cloud_storage.upload_object(UploadObjectDTO(
        bucket=app_settings.cloud_settings.platforms_bucket_name,
        filename=f"{event.photo[-1].file_id}.jpg",
        file=photo,
    ))
    await platform_service.create_platform(CreatePlatformDTO(
        name=dialog_manager.dialog_data["name"],
        image_url=image.url,
        description=dialog_manager.dialog_data["description"],
        login_data=dialog_manager.dialog_data["login_data"],
    ))

    await dialog_manager.switch_to(state=PlatformManagementSG.PLATFORM_LIST)


async def back_to_platform(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    platform_id = dialog_manager.dialog_data.get("platform_id")
    if platform_id is None:
        platform_id = dialog_manager.dialog_data.get("platform_id")

    await dialog_manager.switch_to(state=PlatformManagementSG.PLATFORM)



async def start_edit_platform(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    platform_id = dialog_manager.dialog_data.get("platform_id")

    await dialog_manager.switch_to(state=PlatformManagementSG.PLATFORM)


async def start_platform_products(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=PlatformProductManagementSG.PRODUCT_LIST,
        mode=StartMode.NORMAL,
        data={"platform_id": dialog_manager.dialog_data.get("platform_id")},
        show_mode=ShowMode.EDIT,
    )
