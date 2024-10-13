from typing import Optional
from datetime import datetime, UTC

from src.domain.value_objects.user_topic import CreatedAt, SupergroupChatId, ThreadId
from src.domain.value_objects.user import UserID



class UserTopic:
    __slots__ = (
        'thread_id',
        'user_id',
        'created_at',
        'supergroup_chat_id',
    )

    def __init__(
        self,
        user_id: UserID,
        supergroup_chat_id: SupergroupChatId,
        thread_id: ThreadId,
        created_at: Optional[CreatedAt] = None,
    ) -> None:
        self.user_id = user_id
        self.supergroup_chat_id = supergroup_chat_id
        self.thread_id = thread_id
        self.created_at = created_at or CreatedAt(datetime.now(UTC))

    def __str__(self) -> str:
        return f'UserTopic(user_id={self.user_id}, supergroup_chat_id={self.supergroup_chat_id}, thread_id={self.thread_id}, created_at={self.created_at})'
    
    def __repr__(self) -> str:
        return self.__str__()