from datetime import datetime, UTC
from decimal import Decimal

from sqlalchemy import TIMESTAMP, BigInteger, func, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base


class UserModel(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now,
        default=datetime.now(UTC),
    )
    commission: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    total_withdrawn: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False, default=0)

    orders = relationship('OrderModel', back_populates='user', uselist=True)
    feedbacks = relationship('FeedbackModel', back_populates='user', uselist=True)
