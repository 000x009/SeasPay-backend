from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal.product_application import ProductApplicationDAL
from src.domain.entity.product_application import ProductApplication
from src.infrastructure.data.models import ProductApplicationModel
from src.domain.value_objects.product_application import (
    ProductApplicationID,
    LoginData,
    ProductApplicationCreatedAt,
    ProductApplicationStatus,
)
from src.domain.value_objects.user import UserID
from src.domain.value_objects.purchase_request import PurchaseRequestId


class ProductApplicationDALImpl(ProductApplicationDAL):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product_application: ProductApplication) -> ProductApplication:
        product_application_model = ProductApplicationModel(
            id=product_application.id.value,
            user_id=product_application.user_id.value,
            purchase_request_id=product_application.purchase_request_id.value,
            created_at=product_application.created_at.value,
            login_data=product_application.login_data.value,
            status=product_application.status.value,
        )
        self.session.add(product_application_model)

        return product_application

    async def get_one(self, id: ProductApplicationID) -> ProductApplication:
        query = select(ProductApplicationModel).filter_by(id=id.value)
        result = await self.session.execute(query)
        product_application_model = result.scalar_one_or_none()
        
        return ProductApplication(
            id=ProductApplicationID(product_application_model.id),
            user_id=UserID(product_application_model.user_id),
            purchase_request_id=PurchaseRequestId(product_application_model.purchase_request_id),
            login_data=LoginData(product_application_model.login_data),
            created_at=ProductApplicationCreatedAt(product_application_model.created_at),
            status=ProductApplicationStatus(product_application_model.status),
        )

    async def get_one_by_request_id(self, purchase_request_id: PurchaseRequestId) -> ProductApplication:
        query = (
            select(ProductApplicationModel).filter_by(purchase_request_id=purchase_request_id.value)
        )
        result = await self.session.execute(query)
        product_application_model = result.scalar_one_or_none()

        return ProductApplication(
            id=ProductApplicationID(product_application_model.id),
            user_id=UserID(product_application_model.user_id),
            purchase_request_id=PurchaseRequestId(product_application_model.purchase_request_id),
            login_data=LoginData(product_application_model.login_data),
            created_at=ProductApplicationCreatedAt(product_application_model.created_at),
            status=ProductApplicationStatus(product_application_model.status),
        )

    async def update(self, product_application: ProductApplication) -> ProductApplication:
        product_application_model = ProductApplicationModel(
            id=product_application.id.value,
            user_id=product_application.user_id.value,
            purchase_request_id=product_application.purchase_request_id.value,
            created_at=product_application.created_at.value,
            login_data=product_application.login_data.value,
            status=product_application.status.value,
        )
        await self.session.merge(product_application_model)

        return product_application
