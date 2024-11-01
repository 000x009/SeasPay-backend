from src.application.common.uow import UoW
from src.application.dto.digital_product_details import (
    GetDigitalProductDetailsDTO,
    DigitalProductDetailsDTO,
)
from src.infrastructure.dal.digital_product_details import DigitalProductDetailsDAL
from src.domain.entity.digital_product_details import DigitalProductDetails
from src.domain.value_objects.digital_product_details import (
    LoginData,
    PurchaseURL,
    Commission,
)
from src.domain.value_objects.order import OrderID


class DigitalProductDetailsService:
    def __init__(
        self,
        uow: UoW,
        dal: DigitalProductDetailsDAL,
    ) -> None:
        self.uow = uow
        self.dal = dal

    async def get(self, data: GetDigitalProductDetailsDTO) -> DigitalProductDetailsDTO:
        details = await self.dal.get(OrderID(data.order_id))

        return DigitalProductDetailsDTO(
            order_id=details.order_id.value,
            purchase_url=details.purchase_url.value,
            commission=details.commission.value,
            login_data=details.login_data.value,
        )

    async def insert(self, data: DigitalProductDetailsDTO) -> DigitalProductDetailsDTO:
        details = await self.dal.insert(DigitalProductDetails(
            order_id=OrderID(data.order_id),
            purchase_url=PurchaseURL(data.purchase_url),
            commission=Commission(data.commission),
            login_data=LoginData(data.login_data),
        ))
        await self.uow.commit()

        return DigitalProductDetailsDTO(
            order_id=details.order_id.value,
            purchase_url=details.purchase_url.value,
            commission=details.commission.value,
            login_data=details.login_data.value,
        )
