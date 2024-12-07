import uuid
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import String, ForeignKey, UUID, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import OrderModel, RequisiteModel


class WithdrawDetailsModel(Base):
    __tablename__ = 'withdraw_details'

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('order.id', ondelete='CASCADE'),
        primary_key=True,
    )
    requisite_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('requisite.id', ondelete='SET NULL'),
        nullable=True,
    )
    payment_receipt: Mapped[str] = mapped_column(String, nullable=False)
    commission: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)

    order: Mapped['OrderModel'] = relationship(back_populates='withdraw_details', uselist=False)
    requisite: Mapped['RequisiteModel'] = relationship(back_populates='withdraw_details', uselist=False)
