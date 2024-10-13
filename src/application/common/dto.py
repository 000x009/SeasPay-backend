from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pagination:
    limit: int
    offset: int


@dataclass
class FileDTO:
    input_file: bytes
    filename: Optional[str] = field(default=None)
