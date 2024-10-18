from typing import Optional
import json
from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr, model_validator

from src.domain.value_objects.withdraw_method import MethodEnum


class CreateWithdrawOrderSchema(BaseModel):
    method: MethodEnum
    card_number: Optional[str] = Field(default=None)
    card_holder_name: Optional[str] = Field(default=None)
    crypto_address: Optional[str] = Field(default=None)
    crypto_network: Optional[str] = Field(default=None)

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class CreateTransferOrderSchema(BaseModel):
    receiver_email: EmailStr
    amount: Decimal
