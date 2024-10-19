from src.domain.value_objects.order import OrderID, OrderType
from src.domain.value_objects.digital_product_details import PurchaseURL, Commission


class DigitalProductDetails:
    __slots__ = (
        'order_id',
        'type_',
        'product_url',
        'commission',
    )

    def __init__(
        self,
        order_id: OrderID,
        type_: OrderType,
        purchase_url: PurchaseURL,
        commission: Commission,
    ) -> None:
        self.order_id = order_id
        self.type_ = type_
        self.purchase_url = purchase_url
        self.commission = commission
