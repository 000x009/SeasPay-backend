from typing import Optional, TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import PlatformModel


class PlatformProductModel(Base):
    __tablename__ = 'platform_product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    platform_id: Mapped[int] = mapped_column(Integer, ForeignKey('platform.id'), nullable=False)
    purchase_url: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    instruction: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)

    platform: Mapped['PlatformModel'] = relationship(back_populates='products', uselist=False)
