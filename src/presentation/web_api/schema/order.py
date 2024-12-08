from typing import Dict, Optional
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class CreateWithdrawOrderSchema(BaseModel):
    requisite_id: UUID
    payment_receipt_url: str


class CreateTransferOrderSchema(BaseModel):
    receiver_email: EmailStr
    amount: Decimal
    payment_receipt_url: Optional[str] = Field(default=None)
    payment_id: Optional[UUID] = Field(default=None)


class CreateDigitalProductOrderSchema(BaseModel):
    application_id: UUID
    login_data: Dict[str, str]
    payment_id: Optional[UUID] = Field(default=None)
    payment_receipt_url: Optional[str] = Field(default=None)


class PurchasePlatformProductSchema(BaseModel):
    product_id: int
    login_data: Dict[str, str]
    payment_receipt_url: Optional[str] = Field(default=None)
    payment_id: Optional[UUID] = Field(default=None)


class PurchasePlatformProductCryptoSchema(BaseModel):
    product_id: int
    payment_id: UUID
    login_data: Dict[str, str]
