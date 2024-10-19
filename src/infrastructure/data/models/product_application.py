import uuid
from typing import TYPE_CHECKING, Dict, List
from datetime import datetime

from sqlalchemy import TIMESTAMP, func, UUID, ForeignKey, BigInteger, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.value_objects.product_application import ProductApplicationStatusEnum

if TYPE_CHECKING:
    from src.infrastructure.data.models import UserModel, PurchaseRequestModel


class ProductApplicationModel(Base):
    __tablename__ = 'product_application'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.user_id'))
    purchase_request_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('purchase_request.id'))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    required_fields: Mapped[Dict[str, List[str]]] = mapped_column(JSON)
    status: Mapped[ProductApplicationStatusEnum] = mapped_column(
        Enum('SENT', 'FULLFILLED', name='product_application_status'),
        default=ProductApplicationStatusEnum.SENT,
    )

    user: Mapped['UserModel'] = relationship(back_populates='purchase_requests', uselist=False)
    purchase_request: Mapped['PurchaseRequestModel'] = relationship(back_populates='product_applications', uselist=False)
