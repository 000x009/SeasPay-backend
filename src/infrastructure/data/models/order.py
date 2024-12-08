import uuid
from datetime import datetime, UTC
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, BigInteger, ForeignKey, Enum, func, TIMESTAMP, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.value_objects.order import OrderStatusEnum, OrderTypeEnum

if TYPE_CHECKING:
    from src.infrastructure.data.models import (
        UserModel,
        CompletedOrderModel,
        WithdrawDetailsModel,
        TransferDetailsModel,
        DigitalProductDetailsModel,
    )


class OrderModel(Base):
    __tablename__ = 'order'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, autoincrement=False)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    payment_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID,
        ForeignKey('payment.id', ondelete='SET NULL'),
        nullable=True,
    )
    payment_receipt: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=datetime.now(UTC),
    )
    type: Mapped[OrderTypeEnum] = mapped_column(
        Enum('WITHDRAW', 'TRANSFER', 'DIGITAL_PRODUCT', name='order_type'),
        nullable=False,
    )
    status: Mapped[OrderStatusEnum] = mapped_column(
        Enum("NEW", "PROCESSING", "COMPLETE", "CANCEL", "DELAY", name="order_status"),
        default=OrderStatusEnum.NEW,
        nullable=False,
    )
    telegram_message_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint('type', 'id', name='uq_type_id'),
    )

    user: Mapped['UserModel'] = relationship(back_populates='orders', uselist=False)
    completed_order: Mapped[Optional['CompletedOrderModel']] = relationship(back_populates='order', uselist=False)
    withdraw_details: Mapped['WithdrawDetailsModel'] = relationship(back_populates='order', uselist=False)
    transfer_details: Mapped['TransferDetailsModel'] = relationship(back_populates='order', uselist=False)
    digital_product_details: Mapped['DigitalProductDetailsModel'] = relationship(back_populates='order', uselist=False)
