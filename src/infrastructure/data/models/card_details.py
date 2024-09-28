from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import OrderModel


class CardDetailsModel(Base):
    __tablename__ = 'card_details'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    card_number: Mapped[int] = mapped_column(Integer, nullable=False)
    card_holder_name: Mapped[str] = mapped_column(String(100), nullable=False)

    order: Mapped['OrderModel'] = relationship(back_populates='withdraw_details', uselist=False)
