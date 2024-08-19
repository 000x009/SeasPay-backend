from typing import Optional
from datetime import datetime, UTC

from sqlalchemy import String, Enum, TIMESTAMP, func, DECIMAL, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.data.models import Base
from src.domain.entity.invoice import InvoiceStatus


class InvoiceModel(Base):
    __tablename__ = 'invoice'

    id: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=False)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    subject: Mapped[Optional[str]] = mapped_column(String(length=4000), nullable=True)
    note: Mapped[Optional[str]] = mapped_column(String(length=4000), nullable=True)
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus),
        default=InvoiceStatus.DRAFT,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=datetime.now(UTC),
        nullable=False,
    )
    term: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    recipient_email: Mapped[str] = mapped_column(String, nullable=True)
    amount: Mapped[float] = mapped_column(DECIMAL, nullable=False)
