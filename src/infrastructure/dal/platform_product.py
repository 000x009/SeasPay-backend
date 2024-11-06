from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete

from src.domain.value_objects.platform_product import (
    Instruction,
    Price,
    ImageURL,
    PurchaseURL,
    ProductName,
    PlatformProductID,
)
from src.domain.value_objects.platform import PlatformID
from src.domain.entity.platform_product import PlatformProduct, PlatformProductDB
from src.infrastructure.data.models import PlatformProductModel
from src.application.common.dal.platform_product import PlatformProductDAL


class PlatformProductDALImpl(PlatformProductDAL):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, product_id: PlatformProductID) -> PlatformProductDB:
        query = select(PlatformProductModel).where(PlatformProductModel.id == product_id.value)
        result = await self.session.execute(query)
        platform_product = result.scalar_one()

        return PlatformProductDB(
            platform_product_id=PlatformProductID(platform_product.id),
            platform_id=PlatformID(platform_product.platform_id),
            purchase_url=PurchaseURL(platform_product.purchase_url),
            price=Price(platform_product.price),
            image_url=ImageURL(platform_product.image_url),
            instruction=Instruction(platform_product.instruction),
            name=ProductName(platform_product.name),
        )

    async def insert(self, platform_product: PlatformProduct) -> PlatformProductDB:
        platform_product_model = PlatformProductModel(
            platform_id=platform_product.platform_id.value,
            purchase_url=platform_product.purchase_url.value,
            price=platform_product.price.value,
            image_url=platform_product.image_url.value,
            instruction=platform_product.instruction.value,
            name=platform_product.name.value,
        )

        self.session.add(platform_product_model)

        return PlatformProductDB(
            platform_product_id=PlatformProductID(platform_product_model.id),
            platform_id=PlatformID(platform_product_model.platform_id),
            purchase_url=PurchaseURL(platform_product_model.purchase_url),
            price=Price(platform_product_model.price),
            image_url=ImageURL(platform_product_model.image_url),
            instruction=Instruction(platform_product_model.instruction),
            name=ProductName(platform_product_model.name),
        )

    async def list_(self, platform_id: PlatformID, limit: int, offset: int) -> List[PlatformProductDB]:
        query = (
            select(PlatformProductModel)
            .filter_by(platform_id=platform_id.value)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        platform_products = result.scalars().all()

        return [
            PlatformProductDB(
                platform_product_id=PlatformProductID(platform_product.id),
                platform_id=PlatformID(platform_product.platform_id),
                purchase_url=PurchaseURL(platform_product.purchase_url),
                price=Price(platform_product.price),
                image_url=ImageURL(platform_product.image_url),
                instruction=Instruction(platform_product.instruction),
                name=ProductName(platform_product.name),
            )
            for platform_product in platform_products
        ]

    async def get_total(self, platform_id: PlatformID) -> int:
        query = select(func.count(PlatformProductModel.id)).filter_by(platform_id=platform_id.value)
        result = await self.session.execute(query)

        return result.scalar_one()

    async def delete(self, product_id: PlatformProductID) -> None:
        query = delete(PlatformProductModel).where(PlatformProductModel.id == product_id.value)
        await self.session.execute(query)

    async def update(self, platform_product: PlatformProductDB) -> PlatformProductDB:
        model = PlatformProductModel(
            id=platform_product.platform_product_id.value,
            platform_id=platform_product.platform_id.value,
            purchase_url=platform_product.purchase_url.value,
            price=platform_product.price.value,
            image_url=platform_product.image_url.value,
            instruction=platform_product.instruction.value,
            name=platform_product.name.value,
        )

        await self.session.merge(model)

        return PlatformProductDB(
            platform_product_id=PlatformProductID(model.id),
            platform_id=PlatformID(model.platform_id),
            purchase_url=PurchaseURL(model.purchase_url),
            price=Price(model.price),
            image_url=ImageURL(model.image_url),
            instruction=Instruction(model.instruction),
            name=ProductName(model.name),
        )
