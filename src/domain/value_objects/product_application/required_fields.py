from typing import Dict, List
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject



@dataclass(frozen=True)
class ProductApplicationRequiredFields(ValueObject[Dict[str, List[str]]]):
  value: Dict[str, List[str]]
