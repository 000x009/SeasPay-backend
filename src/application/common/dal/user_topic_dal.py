from typing import Optional, Protocol
from abc import abstractmethod

from src.domain.entity.user_topic import UserTopic
from src.domain.value_objects.user import UserID
from src.domain.value_objects.user_topic import ThreadId



class UserTopicDAL(Protocol):
    @abstractmethod
    async def insert(self, user_topic: UserTopic) -> UserTopic:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UserID) -> Optional[UserTopic]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, thread_id: ThreadId) -> Optional[UserTopic]:
        raise NotImplementedError
