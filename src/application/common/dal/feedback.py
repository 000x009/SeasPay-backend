from typing import Protocol
from abc import abstractmethod


class BaseFeedbackDAL(Protocol):
    @abstractmethod
    async def insert(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self):
        raise NotImplementedError

    @abstractmethod
    async def list_(self, limit: int, offset: int):
        raise NotImplementedError
