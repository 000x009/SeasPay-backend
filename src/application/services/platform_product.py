from src.application.dto.platform_product import (
    PlatformProductDTO,
    GetPlatformProductDTO,
    ListPlatformProductDTO,
    AddPlatformProductDTO,
    ListPlatformProductResultDTO,
    DeletePlatformProductDTO,
    UpdatePlatformProductDTO,
)
from src.infrastructure.dal.platform_product import PlatformProductDAL
from src.application.common.uow import UoW
from src.domain.value_objects.platform import PlatformID
from src.domain.value_objects.platform_product import PlatformProductID
from src.application.services.product_application import ProductApplicationService
from src.domain.entity.platform_product import PlatformProduct, PlatformProductDB
from src.domain.value_objects.platform_product import PurchaseURL, Price, ImageURL, Instruction, ProductName


class PlatformProductService:
    def __init__(
        self,
        uow: UoW,
        platform_product_dal: PlatformProductDAL,
        product_application_service: ProductApplicationService,
    ) -> None:
        self.uow = uow
        self.platform_product_dal = platform_product_dal
        self.product_application_service = product_application_service

    async def get_platform_product(self, data: GetPlatformProductDTO) -> PlatformProductDTO:
        platform_product = await self.platform_product_dal.get(PlatformProductID(data.id))

        return PlatformProductDTO(
            id=platform_product.platform_product_id.value,
            platform_id=platform_product.platform_id.value,
            purchase_url=platform_product.purchase_url.value,
            price=platform_product.price.value,
            instruction=platform_product.instruction.value,
            image_url=platform_product.image_url.value,
            name=platform_product.name.value,
        )

    async def list_platform_product(self, data: ListPlatformProductDTO) -> ListPlatformProductResultDTO:
        platform_products = await self.platform_product_dal.list_(
            platform_id=PlatformID(data.platform_id),
            limit=data.pagination.limit,
            offset=data.pagination.offset,
        )
        total = await self.platform_product_dal.get_total(PlatformID(data.platform_id))

        return ListPlatformProductResultDTO(
            total=total,
            products=[
                PlatformProductDTO(
                    id=platform_product.platform_product_id.value,
                    platform_id=platform_product.platform_id.value,
                    purchase_url=platform_product.purchase_url.value,
                    price=platform_product.price.value,
                    instruction=platform_product.instruction.value,
                    image_url=platform_product.image_url.value,
                    name=platform_product.name.value,
                )
                for platform_product in platform_products
            ],
        )

    async def add_platform_product(self, data: AddPlatformProductDTO) -> PlatformProductDTO:
        platform_product = PlatformProduct(
            name=ProductName(data.name),
            platform_id=PlatformID(data.platform_id),
            purchase_url=PurchaseURL(data.purchase_url),
            price=Price(data.price),
            image_url=ImageURL(data.image_url),
            instruction=Instruction(data.instruction),
        )
        platform_product = await self.platform_product_dal.insert(platform_product)
        await self.uow.commit()

        return PlatformProductDTO(
            id=platform_product.platform_product_id.value,
            platform_id=platform_product.platform_id.value,
            purchase_url=platform_product.purchase_url.value,
            price=platform_product.price.value,
            instruction=platform_product.instruction.value,
            name=platform_product.name.value,
            image_url=platform_product.image_url.value,
        )

    async def delete_platform_product(self, data: DeletePlatformProductDTO) -> None:
        await self.platform_product_dal.delete(PlatformProductID(data.id))
        await self.uow.commit()
        
    async def update_platform_product(self, data: UpdatePlatformProductDTO) -> PlatformProductDTO:
        platform_product = PlatformProductDB(
            platform_product_id=PlatformProductID(data.product_id),
            platform_id=PlatformID(data.platform_id),
            purchase_url=PurchaseURL(data.purchase_url),
            name=ProductName(data.name),
            price=Price(data.price),
            image_url=ImageURL(data.image_url),
            instruction=Instruction(data.instruction),
        )
        platform_product = await self.platform_product_dal.update(platform_product)
        await self.uow.commit()

        return PlatformProductDTO(
            id=platform_product.platform_product_id.value,
            platform_id=platform_product.platform_id.value,
            purchase_url=platform_product.purchase_url.value,
            price=platform_product.price.value,
            instruction=platform_product.instruction.value,
            image_url=platform_product.image_url.value,
            name=platform_product.name.value,
        )
