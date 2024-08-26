from aiohttp import ClientSession

from src.application.services.paypal import PayPalAuthClient
from src.infrastructure.config import PayPal


class PayPalAuthClientImpl(PayPalAuthClient):
    def __init__(
        self,
        settings: PayPal
    ):
        self.settings = settings
        self._session = ClientSession(
            base_url=settings.api_base_url,
        )

    async def oauth(self):
        pass
