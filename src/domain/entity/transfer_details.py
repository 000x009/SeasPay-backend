from src.domain.value_objects.order import OrderID
from src.domain.value_objects.transfer_details import ReceiptPhotoURL, ReceiverEmail, TransferAmount, Commission


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
