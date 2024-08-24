from decimal import Decimal
from datetime import datetime, UTC

from pydantic import BaseModel, Field

from src.domain.entity.order import OrderStatus


class CreateOrderSchema(BaseModel):
    invoice_id: int
    payment_receipt: str
    final_amount: Decimal
    time: datetime = Field(default=datetime.now(UTC))
    status: OrderStatus = Field(default=OrderStatus.WAIT)
