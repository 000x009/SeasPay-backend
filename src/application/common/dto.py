from dataclasses import dataclass, field
from typing import BinaryIO, Optional


@dataclass
class Pagination:
    limit: int
    offset: int


@dataclass
class FileDTO:
    input_file: BinaryIO
    filename: Optional[str] = field(default=None)
