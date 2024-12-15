import uuid
from typing import TYPE_CHECKING, Optional
from decimal import Decimal

from sqlalchemy import String, ForeignKey, UUID, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import OrderModel


class TransferDetailsModel(Base):
    __tablename__ = 'transfer_details'

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey('order.id', ondelete='CASCADE'), primary_key=True
    )
    receiver_email: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    receipt_photo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    commission: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)

    order: Mapped['OrderModel'] = relationship(back_populates='transfer_details', uselist=False)
