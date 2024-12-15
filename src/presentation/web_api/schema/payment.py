from decimal import Decimal

from pydantic import BaseModel


class CreateCryptoPayInvoiceSchema(BaseModel):
    amount: Decimal
