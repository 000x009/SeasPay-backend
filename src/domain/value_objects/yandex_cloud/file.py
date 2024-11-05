from typing import BinaryIO
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class File(ValueObject[BinaryIO | bytes]):
    value: BinaryIO | bytes
