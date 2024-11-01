import uuid
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import String, ForeignKey, Enum, UUID, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import OrderModel


class WithdrawDetailsModel(Base):
    __tablename__ = 'withdraw_details'

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('order.id', ondelete='CASCADE'),
        primary_key=True,
    )
    payment_receipt: Mapped[str] = mapped_column(String, nullable=False)
    method: Mapped[str] = mapped_column(Enum("CARD", "CRYPTO", name="method_enum"), nullable=False)
    card_number: Mapped[str] = mapped_column(String(20), nullable=True)
    card_holder_name: Mapped[str] = mapped_column(String, nullable=True)
    crypto_address: Mapped[str] = mapped_column(String, nullable=True)
    crypto_network: Mapped[str] = mapped_column(String, nullable=True)
    commission: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)

    order: Mapped['OrderModel'] = relationship(back_populates='withdraw_details', uselist=False)
