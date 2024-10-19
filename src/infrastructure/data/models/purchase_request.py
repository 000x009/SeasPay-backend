import uuid
from typing import TYPE_CHECKING
from datetime import datetime, UTC

from sqlalchemy import TIMESTAMP, func, UUID, String, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import UserModel


class PurchaseRequestModel(Base):
    __tablename__ = 'purchase_request'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.user_id'))
    purchase_url: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    
    user: Mapped['UserModel'] = relationship(back_populates='purchase_requests', uselist=False)
