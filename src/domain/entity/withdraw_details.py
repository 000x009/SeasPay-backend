from typing import Optional
from decimal import Decimal

from src.domain.value_objects.order import OrderID, MustReceiveAmount
from src.domain.value_objects.withdraw_method import (
    Method,
    PaymentReceipt,
    WithdrawCommission,
)
from src.domain.value_objects.requisite import RequisiteId
from src.domain.value_objects.user import TotalWithdrawn
from src.domain.value_objects.completed_order import PaymentSystemReceivedAmount
from src.infrastructure.config import app_settings


class WithdrawDetails:
    __slots__ = (
        'order_id',
        'requisite_id',
        'payment_receipt',
        'commission',
    )

    def __init__(
        self,
        order_id: OrderID,
        requisite_id: Optional[RequisiteId] = None,
        payment_receipt: Optional[PaymentReceipt] = None,
        commission: Optional[WithdrawCommission] = None,
    ) -> None:
        self.order_id = order_id
        self.requisite_id = requisite_id
        self.payment_receipt = payment_receipt
        self.commission = commission

    def set_commission(
        self,
        payment_system_received_amount: PaymentSystemReceivedAmount,
        user_total_withdrawn: TotalWithdrawn,
    ) -> Optional[WithdrawCommission]:
        total_withdrawn = TotalWithdrawn(user_total_withdrawn.value + payment_system_received_amount.value)
        min_commission = app_settings.commission.min_withdraw_percentage
        commission = self.commission.value

        if total_withdrawn.value > 500:
            commission = min_commission
        elif total_withdrawn.value > 300:
            commission = 8
        elif total_withdrawn.value > 200:
            commission = 9
        elif total_withdrawn.value > 150:
            commission = 10
        elif total_withdrawn.value > 100:
            commission = 11
        elif total_withdrawn.value > 70:
            commission = 12
        elif total_withdrawn.value > 50:
            commission = 13
        elif total_withdrawn.value > 30:
            commission = 14

        self.commission = WithdrawCommission(Decimal(commission))
        return self.commission

    def calculate_amount_user_must_receive(
        self,
        payment_system_received_amount: PaymentSystemReceivedAmount,
    ) -> MustReceiveAmount:
        commission_percentage = Decimal(self.commission.value / 100)
        commission_amount = payment_system_received_amount.value * commission_percentage
        user_amount = payment_system_received_amount.value - commission_amount

        return MustReceiveAmount(round(user_amount, 2))
