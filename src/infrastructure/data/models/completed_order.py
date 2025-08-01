import uuid
from datetime import datetime, UTC
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import Integer, DECIMAL, func, TIMESTAMP, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import OrderModel


class CompletedOrderModel(Base):
    __tablename__ = 'completed_order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('order.id', ondelete='CASCADE'),
        nullable=False,
    )
    payment_system_received_amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)
    user_received_amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=datetime.now(UTC),
    )

    order: Mapped['OrderModel'] = relationship(back_populates='completed_order', uselist=False)
