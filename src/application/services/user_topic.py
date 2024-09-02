from typing import Optional

from src.infrastructure.dal import UserTopicDAL
from src.application.dto.user_topic import CreateUserTopicDTO, GetUserTopicDTO, GetUserTopicByUserIdDTO, UserTopicDTO
from src.domain.entity.user_topic import UserTopic
from src.domain.value_objects.user_topic import ThreadId, SupergroupChatId, CreatedAt
from src.domain.value_objects.user import UserID
from src.domain.exceptions.user_topic import TopicNotFoundError
from src.infrastructure.telegram import TelegramTopicManager


class UserTopicService:
    def __init__(self, user_topic_dal: UserTopicDAL, telegram_topic_manager: TelegramTopicManager):
        self.user_topic_dal = user_topic_dal
        self._telegram_topic_manager = telegram_topic_manager

    async def create_user_topic(self, data: CreateUserTopicDTO) -> UserTopicDTO:
        user_topic = await self._telegram_topic_manager.create_topic(
                name=data.username,
            )
        topic = await self.user_topic_dal.create_user_topic(
            UserTopic(
                user_id=UserID(data.user_id),
                supergroup_chat_id=SupergroupChatId(data.supergroup_chat_id),
                thread_id=ThreadId(user_topic.message_thread_id),
                created_at=CreatedAt(data.created_at),
            )
        )

        return UserTopicDTO(
            user_id=topic.user_id.value,
            supergroup_chat_id=topic.supergroup_chat_id.value,
            thread_id=topic.thread_id.value,
            created_at=topic.created_at.value,
        )

    async def get_user_topic(self, data: GetUserTopicDTO) -> Optional[UserTopicDTO]:
        topic = await self.user_topic_dal.get(ThreadId(data.thread_id))
        if topic is None:
            raise TopicNotFoundError(f"Topic not found for thread {data.thread_id}")

        return UserTopicDTO(
            user_id=topic.user_id.value,
            supergroup_chat_id=topic.supergroup_chat_id.value,
            thread_id=topic.thread_id.value,
            created_at=topic.created_at.value,
        )

    async def get_user_topic_by_user_id(self, data: GetUserTopicByUserIdDTO) -> Optional[UserTopicDTO]:
        topic = await self.user_topic_dal.get_by_user_id(UserID(data.user_id))
        if topic is None:
            return None

        return UserTopicDTO(
            user_id=topic.user_id.value,
            supergroup_chat_id=topic.supergroup_chat_id.value,
            thread_id=topic.thread_id.value,
            created_at=topic.created_at.value,
        )
