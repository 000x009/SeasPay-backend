import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.value_objects.requisite import RequisiteTypeEnum

if TYPE_CHECKING:
    from src.infrastructure.data.models import RequisiteModel


class CryptoRequisiteModel(Base):
    __tablename__ = 'crypto_requisite'

    requisite_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('requisite.id', ondelete='CASCADE'), primary_key=True)
    type: Mapped[RequisiteTypeEnum] = mapped_column(
        Enum("card", "crypto", name="requisite_type"),
        server_default=RequisiteTypeEnum.CRYPTO.value,
    )
    wallet_address: Mapped[str] = mapped_column(String, nullable=False)
    network: Mapped[str] = mapped_column(String, nullable=False)
    asset: Mapped[str] = mapped_column(String, nullable=False)
    memo: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    requisite: Mapped["RequisiteModel"] = relationship(back_populates='crypto_requisite')
