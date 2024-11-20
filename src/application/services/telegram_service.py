from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from src.application.services.user_topic import UserTopicService
from src.application.dto.user_topic import GetUserTopicByUserIdDTO, CreateUserTopicDTO
from src.application.dto.telegram import (
    SendMessageDTO,
    SendPurchaseRequestMessageDTO,
    SavePreparedInlineMessageDTO,
    PreparedInlineMessageDTO,
)
from src.infrastructure.config import load_bot_settings
from src.application.common.telegram import TelegramClientInterface


class TelegramService:
    def __init__(
        self,
        telegram_client: TelegramClientInterface,
        user_topic_service: UserTopicService,
    ) -> None:
        self._telegram_client = telegram_client
        self._user_topic_service = user_topic_service
        self._config = load_bot_settings()

    async def send_message(self, data: SendMessageDTO) -> Message:
        user_topic = await self._user_topic_service.get_user_topic_by_user_id(
            GetUserTopicByUserIdDTO(user_id=data.user_id)
        )
        if user_topic is None:
            topic = await self._telegram_client.create_topic(name=data.username)
            user_topic = await self._user_topic_service.create_user_topic(
                CreateUserTopicDTO(
                    user_id=data.user_id,
                    supergroup_chat_id=self._config.orders_group_id,
                    thread_id=topic.message_thread_id,
                    username=data.username,
                )
            )

        if data.photo is not None:
            message: Message = await self._telegram_client.send_message_photo(
                thread_id=user_topic.thread_id,
                photo=data.photo.input_file,
                filename=data.photo.filename,
                caption=data.text,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text='🗃️ Взяться за заказ', callback_data=f"take_order:{data.order_id}")]
                    ]
                ),  
            )
        else:
            message = await self._telegram_client.send_topic_message(
                thread_id=user_topic.thread_id,
                message=data.text,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text='🗃️ Взяться за заказ', callback_data=f"take_order:{data.order_id}")]
                    ]   
                ),
            )

        return message

    async def send_purchase_request_message(self, data: SendPurchaseRequestMessageDTO) -> Message:
        user_topic = await self._user_topic_service.get_user_topic_by_user_id(
            GetUserTopicByUserIdDTO(user_id=data.user_id)
        )
        if user_topic is None:
            topic = await self._telegram_client.create_topic(name=data.username)
            user_topic = await self._user_topic_service.create_user_topic(
                CreateUserTopicDTO(
                    user_id=data.user_id,
                    supergroup_chat_id=self._config.orders_group_id,
                    thread_id=topic.message_thread_id,
                    username=data.username,
                )
            )

        if data.photo is not None:
            message: Message = await self._telegram_client.send_message_photo(
                thread_id=user_topic.thread_id,
                photo=data.photo.input_file,
                filename=data.photo.filename,
                caption=data.text,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text='🗃️ Обработать запрос', callback_data=f"take_purchase_request:{data.request_id}")]
                    ]
                ),
            )
        else:
            message = await self._telegram_client.send_topic_message(
                thread_id=user_topic.thread_id,
                message=data.text,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text='🗃️ Обработать запрос', callback_data=f"take_purchase_request:{data.request_id}")]
                    ]
                ),
            )

        return message

    async def save_prepared_inline_message(self, data: SavePreparedInlineMessageDTO) -> PreparedInlineMessageDTO:
        prepared_message = await self._telegram_client.save_prepared_inline_message(
            user_id=data.user_id,
            title=data.title,
            message_text=data.message_text,
        )

        return PreparedInlineMessageDTO(prepared_message_id=prepared_message.id)
