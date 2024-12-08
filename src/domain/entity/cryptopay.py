from typing import Optional

from src.domain.value_objects.cryptopay import (
    Amount,
    Asset,
    CurrencyType,
    Fiat,
    InvoiceID,
    InvoiceURL,
    PaidAmount,
    PaidAt,
    InvoiceStatus,
    ExpirationDate,
)
from src.domain.value_objects.payment import PaymentID


class Invoice:
    __slots__ = (
        "payment_id",
        "currency_type",
        "asset",
        "fiat",
        "amount",
    )

    def __init__(
        self,
        payment_id: PaymentID,
        currency_type: CurrencyType,
        amount: Amount,
        asset: Optional[Asset] = None,
        fiat: Optional[Fiat] = None,
    ) -> None:
        self.payment_id = payment_id
        self.currency_type = currency_type
        self.asset = asset
        self.fiat = fiat
        self.amount = amount


class ActiveInvoice(Invoice):
    __slots__ = (
        "id",
        "url",
        "paid_amount",
        "status",
        "paid_at",
        "expiration_date",
    )
    
    def __init__(
        self,
        payment_id: PaymentID,
        currency_type: CurrencyType,
        amount: Amount,
        id: Optional[InvoiceID],
        url: Optional[InvoiceURL],
        paid_amount: Optional[PaidAmount],
        status: Optional[InvoiceStatus],
        paid_at: Optional[PaidAt],
        expiration_date: Optional[ExpirationDate],
        asset: Optional[Asset] = None,
        fiat: Optional[Fiat] = None,
    ) -> None:
        super().__init__(payment_id, currency_type, amount, asset, fiat)
        self.id = id
        self.url = url
        self.paid_amount = paid_amount
        self.status = status
        self.paid_at = paid_at
        self.expiration_date = expiration_date
