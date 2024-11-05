from typing import List, Optional
from dataclasses import dataclass, field

from src.application.common.dto import Pagination


@dataclass(frozen=True)
class PlatformDTO:
    platform_id: int
    name: str
    image_url: str
    web_place: int
    description: Optional[str] = field(default=None)
    login_data: Optional[List[str]] = field(default=None)


@dataclass(frozen=True)
class CreatePlatformDTO:
    name: str
    image_url: str
    web_place: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)
    login_data: Optional[List[str]] = field(default=None)


@dataclass(frozen=True)
class PlatformListResultDTO:
    total: int
    platforms: List[PlatformDTO]


@dataclass(frozen=True)
class GetPlatformDTO:
    platform_id: int


@dataclass(frozen=True)
class ListPlatformDTO:
    pagination: Pagination


@dataclass(frozen=True)
class DeletePlatformDTO:
    platform_id: int


@dataclass(frozen=True)
class UpdatePlatformDTO:
    platform_id: int
    name: str
    image_url: str
    web_place: int
    description: Optional[str] = field(default=None)
    login_data: Optional[List[str]] = field(default=None)
