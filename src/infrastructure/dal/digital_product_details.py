from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal.digital_product_details import BaseTransferDetailsDAL
from src.domain.value_objects.order import OrderID
from src.infrastructure.data.models import DigitalProductDetailsModel
from src.domain.entity.digital_product_details import DigitalProductDetails
from src.domain.value_objects.digital_product_details import LoginData, PurchaseURL, Commission


class DigitalProductDetailsDAL(BaseTransferDetailsDAL):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert(self, digital_product_details: DigitalProductDetails) -> DigitalProductDetails:
        model = DigitalProductDetailsModel(
            order_id=digital_product_details.order_id.value,
            purchase_url=digital_product_details.purchase_url.value,
            commission=digital_product_details.commission.value,
            login_data=digital_product_details.login_data.value,
        )
        self.session.add(model)

        return digital_product_details

    async def get(self, order_id: OrderID) -> DigitalProductDetails:
        query = select(DigitalProductDetailsModel).filter(DigitalProductDetailsModel.order_id == order_id.value)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        return DigitalProductDetails(
            order_id=OrderID(model.order_id),
            purchase_url=PurchaseURL(model.purchase_url),
            commission=Commission(model.commission),
            login_data=LoginData(model.login_data),
        )
