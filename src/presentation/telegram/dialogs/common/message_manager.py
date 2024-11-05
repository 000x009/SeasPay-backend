from typing import Any, Coroutine
import logging

from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.manager.message_manager import MessageManager

from dishka import AsyncContainer, Scope

from aiogram import Bot
from aiogram.types import InputFile
from aiogram.types import BufferedInputFile

from src.application.services.cloud import CloudService
from src.application.dto.cloud import GetObjectDTO


class YandexStorageMedia(MessageManager):
    def __init__(self, dishka_container: AsyncContainer) -> None:
        self.container = dishka_container

    async def get_media_source(
        self,
        media: MediaAttachment,
        bot: Bot,
    ) -> Coroutine[Any, Any, InputFile | str]:
        if media.file_id:
            return await super().get_media_source(media, bot)
        if media.url:
            async with self.container(scope=Scope.REQUEST) as container:
                try:
                    cloud_service: CloudService = await container.get(CloudService)
                    storage_object = cloud_service.get_object(GetObjectDTO(url=media.url))
                    return BufferedInputFile(storage_object.file, filename=storage_object.key)
                except Exception as e:
                    logging.error(e)
                finally:
                    await container.close()

        return await super().get_media_source(media, bot)
