from enum import Enum
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject

class RequisiteTypeEnum(Enum):
    CRYPTO = "crypto"
    CARD = "card"


class RequisiteType(ValueObject[RequisiteTypeEnum]):
    value: RequisiteTypeEnum
