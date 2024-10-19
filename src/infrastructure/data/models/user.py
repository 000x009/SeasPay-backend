from typing import List, Optional, TYPE_CHECKING
from datetime import datetime, UTC
from decimal import Decimal

from sqlalchemy import TIMESTAMP, BigInteger, func, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import UserTopicModel


class UserModel(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=datetime.now(UTC),
    )
    withdraw_commission: Mapped[int] = mapped_column(Integer, nullable=True, default=15)
    transfer_commission: Mapped[int] = mapped_column(Integer, nullable=True, default=15)
    product_commission: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True, default=5)
    total_withdrawn: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True, default=0)

    orders = relationship('OrderModel', back_populates='user', uselist=True, lazy='joined')
    feedbacks = relationship('FeedbackModel', back_populates='user', uselist=True, lazy='joined')
    topics: Mapped[Optional[List["UserTopicModel"]]] = relationship(back_populates='user', uselist=True, lazy='joined')
