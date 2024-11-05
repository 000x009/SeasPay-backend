from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Integer, String, JSON, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import PlatformProductModel


class PlatformModel(Base):
    __tablename__ = 'platform'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    web_place: Mapped[int] = mapped_column(Integer, Sequence("web_place_seq", start=1), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    login_data: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)

    products: Mapped[Optional[List['PlatformProductModel']]] = relationship(
        back_populates='platform', uselist=True
    )
