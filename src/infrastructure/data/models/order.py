from datetime import datetime, UTC
from typing import Mapping, Optional, TYPE_CHECKING

from sqlalchemy import Integer, DateTime, String, BigInteger, ForeignKey, DECIMAL, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.entity.order import OrderStatus

if TYPE_CHECKING:
    from src.infrastructure.data.models import UserModel, InvoiceModel, FeedbackModel


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
    final_amount: Mapped[float] = mapped_column(DECIMAL, nullable=False)  # итоговая сумма в usd
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(UTC),
    )
    withdrawal_detail: Mapped[Mapping[str, str]] = mapped_column(JSON, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.WAIT)

    user: Mapped['UserModel'] = relationship(back_populates='order', uselist=False)
    invoice: Mapped['InvoiceModel'] = relationship(back_populates='order', uselist=False)
    feedback: Mapped['FeedbackModel'] = relationship(back_populates='order', uselist=False)
