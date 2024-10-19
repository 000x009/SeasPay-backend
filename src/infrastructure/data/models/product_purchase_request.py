from typing import List, Optional, TYPE_CHECKING
from datetime import datetime, UTC
from decimal import Decimal

from sqlalchemy import TIMESTAMP, BigInteger, func, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.data.models import Base

if TYPE_CHECKING:
    from src.infrastructure.data.models import ProductModel


class ProductPurchaseRequestModel(Base):
    __tablename__ = 'product_purchase_request'