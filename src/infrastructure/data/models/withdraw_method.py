from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import OrderModel


class WithdrawMethodModel(Base):
    __tablename__ = 'withdraw_method'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    method: Mapped[str] = mapped_column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'withdraw_method',
        'polymorphic_on': method,
    }

    order: Mapped['OrderModel'] = relationship(back_populates='withdraw_method', uselist=False)


class CardMethodModel(WithdrawMethodModel):
    __tablename__ = 'card_method'

    id: Mapped[int] = mapped_column(Integer, ForeignKey('withdraw_method.id'), primary_key=True)
    card_number: Mapped[str] = mapped_column(String, nullable=False)
    card_holder_name: Mapped[str] = mapped_column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'card'
    }


class CryptoMethodModel(WithdrawMethodModel):
    __tablename__ = 'crypto_method'

    id: Mapped[int] = mapped_column(Integer, ForeignKey('withdraw_method.id'), primary_key=True)
    crypto_address: Mapped[str] = mapped_column(String, nullable=False)
    network: Mapped[str] = mapped_column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'crypto'
    }
