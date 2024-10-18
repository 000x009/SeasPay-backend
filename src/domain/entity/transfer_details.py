from src.domain.value_objects.order import OrderID, OrderType
from src.domain.value_objects.transfer_details import ReceiptPhotoURL, ReceiverEmail, TransferAmount


class TransferDetails:
    __slots__ = (
        'order_id',
        'type_',
        'receiver_email',
        'amount',
        'receipt_photo_url',
    )

    def __init__(
        self,
        order_id: OrderID,
        type_: OrderType,
        receiver_email: ReceiverEmail,
        amount: TransferAmount,
        receipt_photo_url: ReceiptPhotoURL,
    ) -> None:
        self.order_id = order_id
        self.type_ = type_
        self.receiver_email = receiver_email
        self.amount = amount
        self.receipt_photo_url = receipt_photo_url
