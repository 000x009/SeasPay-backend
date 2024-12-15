from typing import Optional
from decimal import Decimal

from src.domain.value_objects.order import OrderID, MustReceiveAmount
from src.domain.value_objects.withdraw_method import PaymentReceipt, WithdrawCommission
from src.domain.value_objects.requisite import RequisiteId
from src.domain.value_objects.completed_order import PaymentSystemReceivedAmount


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

    def calculate_amount_user_must_receive(
        self,
        payment_system_received_amount: PaymentSystemReceivedAmount,
    ) -> MustReceiveAmount:
        commission_percentage = Decimal(self.commission.value / 100)
        commission_amount = payment_system_received_amount.value * commission_percentage
        user_amount = payment_system_received_amount.value - commission_amount

        return MustReceiveAmount(round(user_amount, 2))
