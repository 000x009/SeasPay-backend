from dataclasses import dataclass
from typing import List

from src.domain.common.value_objects import ValueObject

@dataclass(frozen=True)
class Photo(ValueObject[List[str]]):
    value: List[str]
