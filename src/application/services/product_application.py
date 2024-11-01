import uuid

from src.infrastructure.dal.product_application import ProductApplicationDALImpl
from src.application.common.uow import UoW
from src.application.dto.product_application import (
    CreateProductApplicationDTO,
    GetProductApplicationDTO,
    ProductApplicationDTO,
    GetProductApplicationByRequestIdDTO,
)
from src.domain.entity.product_application import ProductApplication
from src.domain.value_objects.product_application import (
    ProductApplicationID,
    LoginData,
    ProductApplicationCreatedAt,
    ProductApplicationStatus,
    ProductApplicationStatusEnum,
)
from src.domain.value_objects.user import UserID
from src.domain.value_objects.purchase_request import PurchaseRequestId


class ProductApplicationService:
    def __init__(
        self, dal: ProductApplicationDALImpl,
        uow: UoW,
    ) -> None:
        self.dal = dal
        self.uow = uow

    async def create_application(self, data: CreateProductApplicationDTO) -> ProductApplicationDTO:
        product_application = await self.dal.create(ProductApplication(
            id=ProductApplicationID(uuid.uuid4()),
            user_id=UserID(data.user_id),
            purchase_request_id=PurchaseRequestId(data.purchase_request_id),
            login_data=LoginData(data.login_data),
            created_at=ProductApplicationCreatedAt(data.created_at),
            status=ProductApplicationStatus(data.status),
        ))
        await self.uow.commit()

        return ProductApplicationDTO(
            id=product_application.id.value,
            user_id=product_application.user_id.value,
            purchase_request_id=product_application.purchase_request_id.value,
            created_at=product_application.created_at.value,
            login_data=product_application.login_data.value,
            status=product_application.status.value,
        )

    async def get_application_by_id(self, data: GetProductApplicationDTO) -> ProductApplicationDTO:
        product_application = await self.dal.get_one(ProductApplicationID(data.id))

        return ProductApplicationDTO(
            id=product_application.id.value,
            user_id=product_application.user_id.value,
            purchase_request_id=product_application.purchase_request_id.value,
            created_at=product_application.created_at.value,
            login_data=product_application.login_data.value,
            status=product_application.status.value,
        )

    async def get_application_by_request_id(self, data: GetProductApplicationByRequestIdDTO) -> ProductApplicationDTO:
        product_application = await self.dal.get_one_by_request_id(PurchaseRequestId(data.purchase_request_id))

        return ProductApplicationDTO(
            id=product_application.id.value,
            user_id=product_application.user_id.value,
            purchase_request_id=product_application.purchase_request_id.value,
            created_at=product_application.created_at.value,
            login_data=product_application.login_data.value,
            status=product_application.status.value,
        )

    async def fulfill_application(self, data: GetProductApplicationDTO) -> ProductApplicationDTO:
        product_application = await self.dal.get_one(ProductApplicationID(data.id))
        product_application.status = ProductApplicationStatus(ProductApplicationStatusEnum.FULFILLED)
        product_application = await self.dal.update(product_application)

        await self.uow.commit()

        return ProductApplicationDTO(
            id=product_application.id.value,
            user_id=product_application.user_id.value,
            purchase_request_id=product_application.purchase_request_id.value,
            created_at=product_application.created_at.value,
            login_data=product_application.login_data.value,
            status=product_application.status.value,
        )
