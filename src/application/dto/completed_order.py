from dataclasses import dataclass, field
from datetime import datetime, UTC
from decimal import Decimal


@dataclass(frozen=True)
class CompletedOrderDTO:
    order_id: int
    paypal_received_amount: Decimal
    user_received_amount: Decimal
    taken_commission: int
    received_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class AddCompletedOrderDTO:
    order_id: int
    paypal_received_amount: Decimal
    user_received_amount: Decimal
    taken_commission: int
    received_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class GetCompletedOrderDTO:
    id: int
