from pydantic import BaseModel


class CreateCryptoPayInvoiceSchema(BaseModel):
    amount: int
