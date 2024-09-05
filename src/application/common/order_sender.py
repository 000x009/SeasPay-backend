from typing import Protocol
from abc import abstractmethod


class OrderSender(Protocol):
    @abstractmethod
    async def send_order(self) -> None:
        raise NotImplementedError
