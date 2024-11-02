from typing import Optional

from src.domain.value_objects.platform import PlatformID
from src.domain.value_objects.platform_product import (
    Instruction,
    Price,
    ImageURL,
    PurchaseURL,
    ProductName,
    PlatformProductID,
)


class PlatformProduct:
    __slots__ = (
        'platform_id',
        'purchase_url',
        'instruction',
        'price',
        'image_url',
        'name',
    )

    def __init__(
        self,
        platform_id: PlatformID,
        purchase_url: PurchaseURL,
        price: Price,
        name: ProductName,
        image_url: ImageURL,
        instruction: Optional[Instruction] = None,
    ) -> None:
        self.platform_id = platform_id
        self.purchase_url = purchase_url
        self.instruction = instruction
        self.price = price
        self.image_url = image_url
        self.name = name


class PlatformProductDB(PlatformProduct):
    __slots__ = ('platform_product_id',)

    def __init__(
        self,
        platform_product_id: PlatformProductID,
        platform_id: PlatformID,
        purchase_url: PurchaseURL,
        price: Price,
        name: ProductName,
        image_url: ImageURL,
        instruction: Optional[Instruction] = None,
    ) -> None:
        super().__init__(platform_id, purchase_url, price, name, image_url, instruction)
        self.platform_product_id = platform_product_id
