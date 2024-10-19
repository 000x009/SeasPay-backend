from datetime import datetime
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject



@dataclass(frozen=True)
class ProductApplicationCreatedAt(ValueObject[datetime]):
  value: datetime
