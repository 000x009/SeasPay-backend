from aiocryptopay import AioCryptoPay
from aiocryptopay.models.rates import ExchangeRate

from src.application.common.cryptopay import CryptopayClient
from src.domain.entity.cryptopay import Invoice, ActiveInvoice


class CryptopayClientImpl(CryptopayClient):
    def __init__(self, client: AioCryptoPay) -> None:
        self.client = client

    async def create_invoice(self, invoice: Invoice) -> ActiveInvoice:
        response = await self.client.create_invoice(
            amount=str(invoice.amount.value),
            asset=str(invoice.asset.value),
            currency_type=str(invoice.currency_type.value),
            fiat=str(invoice.fiat.value),
            payload=str(invoice.payment_id.value),
        )

        return ActiveInvoice(
            payment_id=invoice.payment_id,
            currency_type=invoice.currency_type,
            amount=invoice.amount,
            asset=invoice.asset,
            fiat=invoice.fiat,
            url=response.mini_app_invoice_url,
            paid_amount=response.paid_amount,
            status=response.status,
            paid_at=response.paid_at,
            expiration_date=response.expiration_date,
            id=response.invoice_id,
        )

    async def get_rub_usd_rate(self) -> ExchangeRate:
        response = await self.client.get_exchange_rates()

        return response[0]
