import json
from decimal import Decimal
from datetime import datetime, UTC
from typing import Union

from pydantic import BaseModel, Field, model_validator

from src.domain.value_objects.order import OrderStatus
from src.domain.value_objects.withdraw_method import MethodEnum

class CardMethodSchema(BaseModel):
    method: MethodEnum
    card_number: str
    card_holder_name: str

class CryptoMethodSchema(BaseModel):
    method: MethodEnum
    crypto_address: str
    network: str

class CreateOrderSchema(BaseModel):
    final_amount: Decimal
    created_at: datetime = Field(default=datetime.now(UTC))
    status: OrderStatus = Field(default=OrderStatus.NEW)
    withdraw_method: Union[CardMethodSchema, CryptoMethodSchema]

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
