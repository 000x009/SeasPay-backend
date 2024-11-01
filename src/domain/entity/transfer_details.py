from decimal import Decimal

from src.domain.value_objects.order import OrderID
from src.domain.value_objects.transfer_details import ReceiptPhotoURL, ReceiverEmail, TransferAmount, Commission
from src.domain.value_objects.completed_order import PaymentSystemReceivedAmount
from src.domain.value_objects.user import TotalWithdrawn
from src.infrastructure.config import app_settings
from src.domain.value_objects.order import MustReceiveAmount


class TransferDetails:
    __slots__ = (
        'order_id',
        'receiver_email',
        'amount',
        'receipt_photo_url',
        'commission',
    )

    def __init__(
        self,
        order_id: OrderID,
        receiver_email: ReceiverEmail,
        amount: TransferAmount,
        receipt_photo_url: ReceiptPhotoURL,
        commission: Commission,
    ) -> None:
        self.order_id = order_id
        self.receiver_email = receiver_email
        self.amount = amount
        self.receipt_photo_url = receipt_photo_url
        self.commission = commission

    def set_commission(
        self,
        payment_system_received_amount: PaymentSystemReceivedAmount,
        user_total_withdrawn: TotalWithdrawn,
    ) -> Commission:
        total_withdrawn = TotalWithdrawn(user_total_withdrawn.value + payment_system_received_amount.value)
        min_commission = app_settings.commission.min_transfer_percentage
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

        self.commission = Commission(Decimal(commission))
        return self.commission

    def calculate_amount_user_must_receive(
        self,
        payment_system_received_amount: PaymentSystemReceivedAmount,
    ) -> MustReceiveAmount:
        commission_percentage = Decimal(self.commission.value / 100)
        commission_amount = payment_system_received_amount.value * commission_percentage
        user_amount = payment_system_received_amount.value - commission_amount

        return MustReceiveAmount(round(user_amount, 2))
