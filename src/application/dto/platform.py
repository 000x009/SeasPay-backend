from typing import List, Optional
from dataclasses import dataclass, field

from src.application.common.dto import Pagination


@dataclass(frozen=True)
class PlatformDTO:
    platform_id: int
    name: str
    image_url: str
    web_place: str
    description: Optional[str] = field(default=None)
    login_data: Optional[List[str]] = field(default=None)


@dataclass(frozen=True)
class GetPlatformDTO:
    platform_id: int


@dataclass(frozen=True)
class ListPlatformDTO:
    pagination: Pagination
