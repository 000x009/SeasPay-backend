from dataclasses import dataclass
from typing import Mapping

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class PostData(ValueObject[Mapping[str, str]]):
    value: Mapping[str, str]
