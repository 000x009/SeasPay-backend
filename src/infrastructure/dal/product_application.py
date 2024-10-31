from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal.product_application import ProductApplicationDAL
from src.domain.entity.product_application import ProductApplication
from src.infrastructure.data.models import ProductApplicationModel
from src.domain.value_objects.product_application import (
    ProductApplicationID,
    ProductApplicationRequiredFields,
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
            required_fields=product_application.required_fields.value,
            status=product_application.status.value,
        )
        self.session.add(product_application_model)

        return product_application

    async def get_one(self, id: ProductApplicationID) -> ProductApplication:
        product_application_model = await self.session.get(ProductApplicationModel, id.value)
        
        return ProductApplication(
            id=ProductApplicationID(product_application_model.id),
            user_id=UserID(product_application_model.user_id),
            purchase_request_id=PurchaseRequestId(product_application_model.purchase_request_id),
            required_fields=ProductApplicationRequiredFields(product_application_model.required_fields),
            created_at=ProductApplicationCreatedAt(product_application_model.created_at),
            status=ProductApplicationStatus(product_application_model.status),
        )
