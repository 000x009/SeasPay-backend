from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.value_objects.withdraw_method import MethodEnum

if TYPE_CHECKING:
    from src.infrastructure.data.models import OrderModel

class WithdrawMethodModel(Base):
    __tablename__ = 'withdraw_method'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    method: Mapped[str] = mapped_column(Enum("CARD", "CRYPTO", name="method_enum"), nullable=False)
    card_number: Mapped[str] = mapped_column(String(20), nullable=True)
    card_holder_name: Mapped[str] = mapped_column(String, nullable=True)
    crypto_address: Mapped[str] = mapped_column(String, nullable=True)
    crypto_network: Mapped[str] = mapped_column(String, nullable=True)

    order: Mapped['OrderModel'] = relationship(back_populates='withdraw_method', uselist=False)
