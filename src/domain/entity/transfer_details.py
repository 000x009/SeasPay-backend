from decimal import Decimal
from typing import Optional

from src.domain.value_objects.order import OrderID
from src.domain.value_objects.transfer_details import ReceiptPhotoURL, ReceiverEmail, TransferAmount, Commission
from src.domain.value_objects.completed_order import PaymentSystemReceivedAmount
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
        commission: Commission,
        receipt_photo_url: Optional[ReceiptPhotoURL] = None,
    ) -> None:
        self.order_id = order_id
        self.receiver_email = receiver_email
        self.amount = amount
        self.receipt_photo_url = receipt_photo_url
        self.commission = commission

    def calculate_amount_user_must_receive(
        self,
        payment_system_received_amount: PaymentSystemReceivedAmount,
    ) -> MustReceiveAmount:
        commission_percentage = Decimal(self.commission.value / 100)
        commission_amount = payment_system_received_amount.value * commission_percentage
        user_amount = payment_system_received_amount.value - commission_amount

        return MustReceiveAmount(round(user_amount, 2))
