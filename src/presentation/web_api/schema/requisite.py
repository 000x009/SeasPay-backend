from typing import Optional

from pydantic import BaseModel


class CreateCryptoRequisiteSchema(BaseModel):
    wallet_address: str
    asset: str
    network: str
    memo: Optional[str] = None


class CreateCardRequisiteSchema(BaseModel):
    number: str
    holder: str
