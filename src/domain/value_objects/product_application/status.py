from dataclasses import dataclass
from enum import StrEnum

from src.domain.common.value_objects import ValueObject


class ProductApplicationStatusEnum(StrEnum):
  SENT = 'SENT'
  FULFILLED = 'FULFILLED'


@dataclass(frozen=True)
class ProductApplicationStatus(ValueObject):
  value: ProductApplicationStatusEnum
