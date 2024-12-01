import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, TIMESTAMP, UUID, func, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.infrastructure.data.models.base import Base
from src.domain.value_objects.requisite import RequisiteTypeEnum

if TYPE_CHECKING:
    from src.infrastructure.data.models import UserModel


class RequisiteModel(Base):
    __tablename__ = "requisites"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.user_id"),
        nullable=False,
    )
    type: Mapped[RequisiteTypeEnum] = mapped_column(
        Enum("card", "crypto", name="requisite_type"), nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=datetime.datetime.now(datetime.UTC),
    )

    user: Mapped["UserModel"] = relationship(back_populates="requisites")
