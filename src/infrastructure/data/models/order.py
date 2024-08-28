from datetime import datetime, UTC
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, BigInteger, ForeignKey, Enum, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.value_objects.order import OrderStatus

if TYPE_CHECKING:
    from src.infrastructure.data.models import UserModel, CompletedOrderModel


class OrderModel(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    payment_receipt: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=datetime.now(UTC),
    )
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.WAIT)

    user: Mapped['UserModel'] = relationship(back_populates='order', uselist=False)
    completed_order: Mapped[Optional['CompletedOrderModel']] = relationship(back_populates='order', uselist=False)
