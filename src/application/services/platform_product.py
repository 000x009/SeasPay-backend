from typing import List

from src.application.dto.platform_product import (
    PlatformProductDTO,
    GetPlatformProductDTO,
    ListPlatformProductDTO,
)
from src.infrastructure.dal.platform_product import PlatformProductDAL
from src.application.common.uow import UoW
from src.domain.value_objects.platform import PlatformID
from src.domain.value_objects.platform_product import PlatformProductID


class PlatformProductService:
    def __init__(self, uow: UoW, platform_product_dal: PlatformProductDAL) -> None:
        self.uow = uow
        self.platform_product_dal = platform_product_dal

    async def get_platform_product(self, data: GetPlatformProductDTO) -> PlatformProductDTO:
        platform_product = await self.platform_product_dal.get(PlatformProductID(data.id))

        return PlatformProductDTO(
            id=platform_product.platform_product_id.value,
            platform_id=platform_product.platform_id.value,
            purchase_url=platform_product.purchase_url.value,
            price=platform_product.price.value,
            instruction=platform_product.instruction.value,
            image_url=platform_product.image_url.value,
        )

    async def list_platform_product(self, data: ListPlatformProductDTO) -> List[PlatformProductDTO]:
        platform_products = await self.platform_product_dal.list_(
            platform_id=PlatformID(data.platform_id),
            limit=data.pagination.limit,
            offset=data.pagination.offset,
        )

        return [
            PlatformProductDTO(
                id=platform_product.platform_product_id.value,
                platform_id=platform_product.platform_id.value,
                purchase_url=platform_product.purchase_url.value,
                price=platform_product.price.value,
                instruction=platform_product.instruction.value,
                image_url=platform_product.image_url.value,
            )
            for platform_product in platform_products
        ]
