from typing import BinaryIO, Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class GetPresignedPostDTO:
    filename: str


@dataclass(frozen=True)
class PresignedPostDTO:
    url: str
    object_url: str
    data: Mapping[str, str]


@dataclass(frozen=True)
class UploadObjectDTO:
    file: BinaryIO
    filename: str
    bucket: str


@dataclass(frozen=True)
class UploadedObjectResultDTO:
    url: str


@dataclass(frozen=True)
class GetObjectDTO:
    url: str


@dataclass(frozen=True)
class ObjectDTO:
    file: BinaryIO
    key: str
    bucket: str
