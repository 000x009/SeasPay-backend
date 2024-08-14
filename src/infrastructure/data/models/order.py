import enum
from datetime import datetime, UTC
from typing import Optional, Mapping

from sqlalchemy import Integer, DateTime, String, BigInteger, ForeignKey, DECIMAL, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base


class OrderStatus(enum.Enum):
    COMPLETE = 'COMPLETE'
    CANCEL = 'CANCEL'
    WAIT = 'WAIT'
    DELAY = 'DELAY'


class OrderModel(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    payment_receipt: Mapped[str] = mapped_column(String, nullable=False)
    final_amount: Mapped[float] = mapped_column(DECIMAL, nullable=False) #итоговая сумма в usd, которую получит пользователь
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(UTC),
    )
    withdrawal_detail: Mapped[Mapping[str, str]] = mapped_column(JSON, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.WAIT)

    user = relationship('UserModel', back_populates='order')
