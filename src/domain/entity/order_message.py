from src.domain.value_objects.order_message import MessageID, Message
from src.domain.entity.receipt_photo import ReceiptPhoto


class OrderMessage:
    __slots__ = (
        'message_id',
        'receipt_photo',
        'message',
    )

    def __init__(
        self,
        message_id: MessageID,
        receipt_photo: ReceiptPhoto,
        message: Message,
    ):
        self.message_id = message_id
        self.receipt_photo = receipt_photo
        self.message = message

    def __str__(self):
        return f'OrderMessage(message_id={self.message_id})'

    def __repr__(self):
        return self.__str__()
