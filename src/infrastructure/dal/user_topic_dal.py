from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal.user_topic_dal import BaseUserTopicDAL
from src.domain.entity.user_topic import UserTopic
from src.domain.value_objects.user import UserID
from src.domain.value_objects.user_topic import ThreadId, SupergroupChatId, CreatedAt
from src.infrastructure.data.models.user_topic import UserTopicModel


class UserTopicDAL(BaseUserTopicDAL):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert(self, user_topic: UserTopic) -> UserTopic:
        user_topic_db = UserTopicModel(
            user_id=user_topic.user_id.value,
            supergroup_chat_id=user_topic.supergroup_chat_id.value,
            thread_id=user_topic.thread_id.value,
            created_at=user_topic.created_at.value,
        )
        self.session.add(user_topic_db)
        await self.session.flush(objects=[user_topic_db])

        return UserTopic(
            user_id=UserID(user_topic_db.user_id),
            supergroup_chat_id=SupergroupChatId(user_topic_db.supergroup_chat_id),
            thread_id=ThreadId(user_topic_db.thread_id),
            created_at=CreatedAt(user_topic_db.created_at),
        )
        
    async def get_by_user_id(self, user_id: UserID) -> Optional[UserTopic]:
        query = select(UserTopicModel).where(UserTopicModel.user_id == user_id.value)
        result = await self.session.execute(query)
        user_topic_db = result.scalar_one_or_none()
        if user_topic_db is None:
            return None

        return UserTopic(
            user_id=UserID(user_topic_db.user_id),
            supergroup_chat_id=SupergroupChatId(user_topic_db.supergroup_chat_id),
            thread_id=ThreadId(user_topic_db.thread_id),
            created_at=CreatedAt(user_topic_db.created_at),
        )

    async def get(self, thread_id: ThreadId) -> Optional[UserTopic]:
        query = select(UserTopicModel).where(UserTopicModel.thread_id == thread_id.value)
        result = await self.session.execute(query)
        user_topic_db = result.scalar_one_or_none()
        if user_topic_db is None:
            return None

        return UserTopic(
            user_id=UserID(user_topic_db.user_id),
            supergroup_chat_id=SupergroupChatId(user_topic_db.supergroup_chat_id),
            thread_id=ThreadId(user_topic_db.thread_id),
            created_at=CreatedAt(user_topic_db.created_at),
        )
