from typing import Protocol
from abc import abstractmethod


class PayPalAuthClient(Protocol):
    @abstractmethod
    async def oauth(self):
        raise NotImplementedError
