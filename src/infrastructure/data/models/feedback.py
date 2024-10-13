from typing import Optional, TYPE_CHECKING
from datetime import datetime, UTC

from sqlalchemy import Integer, BigInteger, ForeignKey, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import UserModel


class FeedbackModel(Base):
    __tablename__ = 'feedback'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    stars: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(String(5000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=datetime.now(UTC),
        nullable=False,
    )
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped['UserModel'] = relationship(back_populates='feedbacks')
