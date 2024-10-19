import uuid
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import TIMESTAMP, func, UUID, String, ForeignKey, BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.domain.value_objects.purchase_request import RequestStatusEnum

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
    status: Mapped[RequestStatusEnum] = mapped_column(
        Enum('PENDING', 'CONFIRMED', 'CANCELLED', name='request_status'),
        default=RequestStatusEnum.PENDING,
    )

    user: Mapped['UserModel'] = relationship(back_populates='purchase_requests', uselist=False)
