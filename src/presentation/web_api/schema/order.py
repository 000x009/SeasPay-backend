from typing import Dict
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CreateWithdrawOrderSchema(BaseModel):
    requisite_id: UUID
    payment_receipt_url: str


class CreateTransferOrderSchema(BaseModel):
    receiver_email: EmailStr
    amount: Decimal
    payment_receipt_url: str


class CreateDigitalProductOrderSchema(BaseModel):
    application_id: UUID
    payment_receipt_url: str
    login_data: Dict[str, str]


class PurchasePlatformProductSchema(BaseModel):
    product_id: int
    payment_receipt_url: str
    login_data: Dict[str, str]
