from datetime import datetime, UTC
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import Integer, DECIMAL, func, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import OrderModel


class CompletedOrderModel(Base):
    __tablename__ = 'completed_order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('order.id', ondelete='CASCADE'),
        nullable=False,
    )
    paypal_received_amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    user_received_amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    received_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=datetime.now(UTC),
    )
    taken_commission: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped['OrderModel'] = relationship(back_populates='completed_order', uselist=False)
