from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import BigInteger, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import UserModel


class UserCommissionModel(Base):
    __tablename__ = 'user_commission'

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.user_id', ondelete='CASCADE'),
        primary_key=True,
    )
    transfer: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    withdraw: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    digital_product: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates='user_commission', uselist=False)
