from src.domain.value_objects.purchase_request import PurchaseURL, PurchaseRequestId
from src.domain.value_objects.user import UserID


class PurchaseRequest:
    __slots__ = (
        'id',
        'user_id',
        'purchase_url',
    )

    def __init__(
        self,
        id: PurchaseRequestId,
        user_id: UserID,
        purchase_url: PurchaseURL,
    ):
        self.id = id
        self.user_id = user_id
        self.purchase_url = purchase_url

