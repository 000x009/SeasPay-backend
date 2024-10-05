import json
from datetime import datetime, UTC
from typing import Optional

from pydantic import BaseModel, Field, model_validator

from src.domain.value_objects.order import OrderStatus
from src.domain.value_objects.withdraw_method import MethodEnum


class WithdrawMethodSchema(BaseModel):
    method: MethodEnum
    card_number: Optional[str] = Field(default=None)
    card_holder_name: Optional[str] = Field(default=None)
    crypto_address: Optional[str] = Field(default=None)
    crypto_network: Optional[str] = Field(default=None)

class CreateOrderSchema(BaseModel):
    created_at: datetime = Field(default=datetime.now(UTC))
    status: OrderStatus = Field(default=OrderStatus.NEW)
    withdraw_method: WithdrawMethodSchema

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
