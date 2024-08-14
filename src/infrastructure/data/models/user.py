import datetime
from typing import Optional

from sqlalchemy import Integer, DateTime, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base


class UserModel(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    joining_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(datetime.UTC),
    )

    order = relationship('PaymentDetailsModel', back_populates='user')
    