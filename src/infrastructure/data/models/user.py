from typing import List, Optional, TYPE_CHECKING
from datetime import datetime, UTC
from decimal import Decimal

from sqlalchemy import TIMESTAMP, BigInteger, func, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import (
        UserTopicModel,
        UserCommissionModel,
        OrderModel,
        FeedbackModel,
    )
    from src.infrastructure.data.models import PurchaseRequestModel
    from src.infrastructure.data.models import ProductApplicationModel


class UserModel(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=datetime.now(UTC),
    )
    total_withdrawn: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True, default=0)
    referral_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    orders: Mapped[Optional[List["OrderModel"]]] = relationship(
        'OrderModel',
        back_populates='user',
        uselist=True,
        lazy='joined',
    )
    feedbacks: Mapped[Optional[List["FeedbackModel"]]] = relationship(
        'FeedbackModel',
        back_populates='user',
        uselist=True,
        lazy='joined',
    )
    topics: Mapped[Optional[List["UserTopicModel"]]] = relationship(
        back_populates='user',
        uselist=True,
        lazy='joined',
    )
    user_commission: Mapped["UserCommissionModel"] = relationship(
        back_populates='user',
        uselist=False,
        lazy='joined',
    )
    purchase_requests: Mapped[Optional[List["PurchaseRequestModel"]]] = relationship(
        back_populates='user', uselist=True, lazy='joined'
    )
    product_applications: Mapped[Optional[List["ProductApplicationModel"]]] = relationship(
        back_populates='user', uselist=True, lazy='joined'
    )
