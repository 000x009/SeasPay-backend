import uuid
from typing import TYPE_CHECKING, Dict

from sqlalchemy import String, ForeignKey, UUID, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import OrderModel


class DigitalProductDetailsModel(Base):
    __tablename__ = 'digital_product_details'

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('order.id', ondelete='CASCADE'),
        primary_key=True,
    )
    purchase_url: Mapped[str] = mapped_column(String, nullable=False)
    commission: Mapped[int] = mapped_column(Integer, nullable=False)
    login_data: Mapped[Dict[str, str]] = mapped_column(JSON, nullable=True)

    order: Mapped['OrderModel'] = relationship(back_populates='digital_product_details', uselist=False)
