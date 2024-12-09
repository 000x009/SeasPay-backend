from src.application.dto.cryptopay import CreateInvoiceDTO, InvoiceDTO, ExchangeRateDTO
from src.application.common.cryptopay import CryptopayClient
from src.domain.value_objects.payment import PaymentID
from src.domain.value_objects.cryptopay import (
    Amount,
    CurrencyType,
    Asset,
    Fiat,
)
from src.domain.entity.cryptopay import Invoice


class CryptopayService:
    def __init__(self, client: CryptopayClient) -> None:
        self.client = client

    async def create(self, data: CreateInvoiceDTO) -> InvoiceDTO:
        invoice = await self.client.create_invoice(
            Invoice(
                payment_id=PaymentID(data.payment_id),
                amount=Amount(data.amount),
                currency_type=CurrencyType(data.currency_type),
                asset=Asset(data.asset),
                fiat=Fiat(data.fiat),
            )
        )

        return InvoiceDTO(
            id=invoice.id,
            amount=invoice.amount,
            paid_amount=invoice.paid_amount,
            payment_id=invoice.payment_id,
            url=invoice.url,
            status=invoice.status,
            paid_at=invoice.paid_at,
            expiration_date=invoice.expiration_date,
            currency_type=invoice.currency_type,
            asset=invoice.asset,
            fiat=invoice.fiat,
        )

    async def get_rub_usd_rate(self) -> ExchangeRateDTO:
        rate = await self.client.get_rub_usd_rate()

        return ExchangeRateDTO(rate=rate.rate)
