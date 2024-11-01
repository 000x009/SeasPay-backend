from src.domain.value_objects.order import OrderID
from src.domain.value_objects.digital_product_details import PurchaseURL, LoginData, Commission


class DigitalProductDetails:
    __slots__ = (
        'order_id',
        'purchase_url',
        'commission',
        'login_data',
    )

    def __init__(
        self,
        order_id: OrderID,
        purchase_url: PurchaseURL,
        commission: Commission,
        login_data: LoginData,
    ) -> None:
        self.order_id = order_id
        self.purchase_url = purchase_url
        self.commission = commission
        self.login_data = login_data
