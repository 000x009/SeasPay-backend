import datetime
import uuid
from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import Enum, TIMESTAMP, UUID, func, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.infrastructure.data.models.base import Base
from src.domain.value_objects.requisite import RequisiteTypeEnum

if TYPE_CHECKING:
    from src.infrastructure.data.models import (
        UserModel,
        CardRequisiteModel,
        CryptoRequisiteModel,
        WithdrawDetailsModel,
    )


class RequisiteModel(Base):
    __tablename__ = "requisite"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.user_id"),
        nullable=False,
    )
    type: Mapped[RequisiteTypeEnum] = mapped_column(
        Enum("card", "crypto", name="requisite_type"),
        server_default=RequisiteTypeEnum.CRYPTO.value,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=datetime.datetime.now(datetime.UTC),
    )

    user: Mapped["UserModel"] = relationship(back_populates="requisites")
    card_requisite: Mapped[Optional["CardRequisiteModel"]] = relationship(back_populates='requisite', uselist=False)
    crypto_requisite: Mapped[Optional["CryptoRequisiteModel"]] = relationship(back_populates='requisite', uselist=False)
    withdraw_details: Mapped[Optional[List["WithdrawDetailsModel"]]] = relationship(back_populates='requisite', uselist=True)
