from typing import Protocol
from abc import abstractmethod

from src.domain.value_objects.feedback import FeedbackID
from src.domain.entity.feedback import Feedback, FeedbackDB


class BaseFeedbackDAL(Protocol):
    @abstractmethod
    async def insert(self, feedback: Feedback) -> FeedbackDB:
        raise NotImplementedError

    @abstractmethod
    async def get(self, feedback_id: FeedbackID):
        raise NotImplementedError

    @abstractmethod
    async def list_(self, limit: int, offset: int):
        raise NotImplementedError
