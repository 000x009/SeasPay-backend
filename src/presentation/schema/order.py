import json
from decimal import Decimal
from datetime import datetime, UTC

from pydantic import BaseModel, Field, model_validator

from src.domain.value_objects.order import OrderStatus


class CreateOrderSchema(BaseModel):
    final_amount: Decimal
    created_at: datetime = Field(default=datetime.now(UTC))
    status: OrderStatus = Field(default=OrderStatus.WAIT)

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
