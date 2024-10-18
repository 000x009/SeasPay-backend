from typing import Optional
import json
from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr, model_validator

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
