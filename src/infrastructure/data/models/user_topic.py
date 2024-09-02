from datetime import datetime, UTC
from decimal import Decimal

from sqlalchemy import TIMESTAMP, BigInteger, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base
from src.infrastructure.data.models.user import UserModel


class UserTopicModel(Base):
    __tablename__ = 'user_topic'

    thread_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    supergroup_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now(UTC),
        server_default=func.now(),
    )

    user: Mapped[UserModel] = relationship(back_populates='topics', uselist=False)
