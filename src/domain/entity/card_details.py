from src.domain.value_objects.order import OrderID
from src.domain.value_objects.card_details import CardHolderName, CardNumber


class CardDetails:
    __slots__ = (
        'order_id',
        'card_number',
        'card_holder_name',
    )

    def __init__(
        self,
        order_id: OrderID,
        card_number: CardNumber,
        card_holder_name: CardHolderName,
    ) -> None:
        self.order_id = order_id
        self.card_number = card_number
        self.card_holder_name = card_holder_name
