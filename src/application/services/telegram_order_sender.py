from aiogram.types import Message

from src.infrastructure.telegram import TelegramTopicManager
from src.application.services.user_topic import UserTopicService
from src.application.dto.user_topic import GetUserTopicByUserIdDTO, CreateUserTopicDTO
from src.application.dto.order import AddTelegramMessageIdDTO, OrderDTO
from src.application.dto.telegram import SendOrderDTO
from src.infrastructure.telegram import TelegramTopicManager
from src.infrastructure.config import load_bot_settings
from src.application.common.order_sender import OrderSender
from src.application.services.order import OrderService


class TelegramOrderSender(OrderSender):
    def __init__(
        self,
        telegram_client: TelegramTopicManager,
        user_topic_service: UserTopicService,
        order_service: OrderService,
    ) -> None:
        self._telegram_client = telegram_client
        self._user_topic_service = user_topic_service
        self._config = load_bot_settings()
        self.order_service = order_service

    async def send_order(self, data: SendOrderDTO) -> OrderDTO:
        user_topic = await self._user_topic_service.get_user_topic_by_user_id(
            GetUserTopicByUserIdDTO(user_id=data.user_id)
        )

        if user_topic is None:
            topic = await self._telegram_client.create_topic(
                name=data.username,
            )
            user_topic = await self._user_topic_service.create_user_topic(
                CreateUserTopicDTO(
                    user_id=data.user_id,
                    supergroup_chat_id=self._config.orders_group_id,
                    thread_id=topic.message_thread_id,
                    username=data.username,
                )
            )

        if data.photo is not None:
            message = await self._telegram_client.send_message_photo(
                thread_id=user_topic.thread_id,
                photo=data.photo.input_file,
                filename=data.photo.filename,
                caption=data.order_text,
                order_id=data.order_id,
            )
            return await self.order_service.add_telegram_message_id(
                AddTelegramMessageIdDTO(order_id=data.order_id, telegram_message_id=message.message_id)
            )
        message = await self._telegram_client.send_topic_message(
            thread_id=user_topic.thread_id,
            message=data.order_text,
            order_id=data.order_id,
        )
        return await self.order_service.add_telegram_message_id(
            AddTelegramMessageIdDTO(order_id=data.order_id, telegram_message_id=message.message_id)
        )
