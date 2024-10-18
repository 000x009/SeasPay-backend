from src.domain.value_objects.order import OrderID, OrderType, Commission
from src.domain.value_objects.digital_product_details import ProductURL


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
        product_url: ProductURL,
        commission: Commission,
    ) -> None:
        self.order_id = order_id
        self.type_ = type_
        self.product_url = product_url
        self.commission = commission
