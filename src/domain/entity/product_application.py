from typing import Optional
from datetime import datetime, UTC

from src.domain.value_objects.product_application import (
  ProductApplicationCreatedAt,
  ProductApplicationID,
  ProductApplicationRequiredFields,
  ProductApplicationStatus,
  ProductApplicationStatusEnum,
)
from src.domain.value_objects.user.user_id import UserID
from src.domain.value_objects.purchase_request import PurchaseRequestId


class ProductApplication:
  __slots__ = (
    'id',
    'user_id',
    'purchase_request_id',
    'created_at',
    'required_fields',
    'status'
  )

  def __init__(
    self,
    id: ProductApplicationID,
    user_id: UserID,
    purchase_request_id: PurchaseRequestId,
    required_fields: ProductApplicationRequiredFields,
    created_at: Optional[ProductApplicationCreatedAt] = None,
    status: Optional[ProductApplicationStatus] = None,
  ) -> None:
    self.id = id
    self.user_id = user_id
    self.purchase_request_id = purchase_request_id
    self.created_at = created_at
    self.required_fields = required_fields
    self.status = status

    if not self.created_at:
      self.created_at = ProductApplicationCreatedAt(datetime.now(UTC))
    if not self.status:
      self.status = ProductApplicationStatus(ProductApplicationStatusEnum.SENT)
