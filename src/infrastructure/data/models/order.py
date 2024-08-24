from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import Integer, String, BigInteger, ForeignKey, DECIMAL, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.entity.order import OrderStatus

if TYPE_CHECKING:
    from src.infrastructure.data.models import UserModel, InvoiceModel


class OrderModel(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    invoice_id: Mapped[Optional[str]] = mapped_column(
        String,
        ForeignKey('invoice.id', ondelete='CASCADE'),
        nullable=True,
    )
    payment_receipt: Mapped[str] = mapped_column(String, nullable=False)
    final_amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)  # итоговая сумма в usd
    time: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        default=datetime.now(UTC),
    )
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.WAIT)

    user: Mapped['UserModel'] = relationship(back_populates='order', uselist=False)
    invoice: Mapped['InvoiceModel'] = relationship(back_populates='order', uselist=False)
