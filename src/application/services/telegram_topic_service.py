from src.infrastructure.telegram import TelegramTopicManager
from src.application.services.user_topic import UserTopicService
from src.application.dto.user_topic import GetUserTopicByUserIdDTO, CreateUserTopicDTO
from src.application.dto.telegram import SendOrderDTO
from src.infrastructure.telegram import TelegramTopicManager
from src.infrastructure.config import BotSettings


class TelegramOrderSender:
    def __init__(
        self,
        client: TelegramTopicManager,
        user_topic_service: UserTopicService,
        telegram_topic_manager: TelegramTopicManager,
        config: BotSettings,
    ) -> None:
        self._client = client
        self._user_topic_service = user_topic_service
        self._telegram_topic_manager = telegram_topic_manager
        self._config = config

    async def send_order(self, data: SendOrderDTO) -> None:
        user_topic = await self._user_topic_service.get_user_topic_by_user_id(
            GetUserTopicByUserIdDTO(user_id=data.user_id)
        )
        if user_topic is None:
            user_topic = await self._user_topic_service.create_user_topic(
                CreateUserTopicDTO(
                    user_id=data.user_id,
                    supergroup_chat_id=self._config.orders_group_id,
                    thread_id=user_topic.message_thread_id,
                    username=data.username,
                )
            )

        await self._telegram_topic_manager.send_topic_message(
            thread_id=user_topic.thread_id,
            message=data.order_text,
        )