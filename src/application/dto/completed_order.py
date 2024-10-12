from dataclasses import dataclass, field
from datetime import datetime, UTC
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CompletedOrderDTO:
    order_id: int
    paypal_received_amount: Decimal
    user_received_amount: Decimal
    completed_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class AddCompletedOrderDTO:
    order_id: int
    paypal_received_amount: Decimal
    user_received_amount: Decimal
    completed_at: datetime = field(default=datetime.now(UTC))


@dataclass(frozen=True)
class GetCompletedOrderDTO:
    id: int


@dataclass(frozen=True)
class TotalWithdrawDTO:
    total_withdraw: Decimal


@dataclass(frozen=True)
class ProfitDTO:
    all_time: Decimal
    month: Decimal
    week: Decimal


@dataclass(frozen=True)
class GetProfitDTO:
    timespan: Optional[float] = field(default=None)
