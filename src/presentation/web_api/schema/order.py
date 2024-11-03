from typing import Optional, Dict
from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr, UUID4

from src.domain.value_objects.withdraw_method import MethodEnum


class CreateWithdrawOrderSchema(BaseModel):
    method: MethodEnum
    payment_receipt_url: str
    card_number: Optional[str] = Field(default=None)
    card_holder_name: Optional[str] = Field(default=None)
    crypto_address: Optional[str] = Field(default=None)
    crypto_network: Optional[str] = Field(default=None)


class CreateTransferOrderSchema(BaseModel):
    receiver_email: EmailStr
    amount: Decimal
    payment_receipt_url: str


class CreateDigitalProductOrderSchema(BaseModel):
    application_id: UUID4
    payment_receipt_url: str
    login_data: Dict[str, str]


class PurchasePlatformProductSchema(BaseModel):
    platform_product_id: UUID4
    payment_receipt_url: str
    login_data: Dict[str, str]
