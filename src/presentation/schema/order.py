from decimal import Decimal
from datetime import datetime, UTC

from pydantic import BaseModel, Field

from src.domain.value_objects.order import OrderStatus


class CreateOrderSchema(BaseModel):
    payment_receipt: str
    time: datetime = Field(default=datetime.now(UTC))
    status: OrderStatus = Field(default=OrderStatus.WAIT)
