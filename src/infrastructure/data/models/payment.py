import uuid
from datetime import datetime, UTC
from typing import TYPE_CHECKING, Optional
from decimal import Decimal

from sqlalchemy import DECIMAL, String, BigInteger, ForeignKey, Enum, func, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.value_objects.payment import PaymentStatusEnum

if TYPE_CHECKING:
    from src.infrastructure.data.models import UserModel


class PaymentModel(Base):
    __tablename__ = 'payment'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, autoincrement=False)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    invoice_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    status: Mapped[PaymentStatusEnum] = mapped_column(
        Enum('ACTIVE', 'PAID', 'FAILED', name='payment_status'),
        default=PaymentStatusEnum.ACTIVE,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=datetime.now(UTC),
    )

    user: Mapped['UserModel'] = relationship(back_populates='payments', uselist=False)
