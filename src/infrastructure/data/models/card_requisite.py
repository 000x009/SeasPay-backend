import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UUID, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.value_objects.requisite import RequisiteTypeEnum

if TYPE_CHECKING:
    from src.infrastructure.data.models import RequisiteModel


class CardRequisiteModel(Base):
    __tablename__ = 'card_requisite'
    
    requisite_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('requisite.id', ondelete='CASCADE'), primary_key=True)
    type: Mapped[RequisiteTypeEnum] = mapped_column(
        Enum("card", "crypto", name="requisite_type"),
        server_default=RequisiteTypeEnum.CARD.value,
    )
    number: Mapped[str] = mapped_column(String(19), nullable=False)
    holder: Mapped[str] = mapped_column(String(100), nullable=False)
    
    requisite: Mapped["RequisiteModel"] = relationship(back_populates='card_requisite')
