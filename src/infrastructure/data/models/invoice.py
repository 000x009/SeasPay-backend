from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import String, Enum, TIMESTAMP, func, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.value_objects.invoice import InvoiceStatus

if TYPE_CHECKING:
    from src.infrastructure.data.models import OrderModel


class InvoiceModel(Base):
    __tablename__ = 'invoice'

    id: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=False)
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('order.id', ondelete='CASCADE'),
        nullable=False,
    )
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus),
        default=InvoiceStatus.SENT,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=datetime.now(UTC),
        nullable=False,
    )

    order: Mapped['OrderModel'] = relationship(back_populates='invoice', uselist=False)
