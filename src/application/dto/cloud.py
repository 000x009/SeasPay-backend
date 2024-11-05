from typing import BinaryIO
from dataclasses import dataclass


@dataclass(frozen=True)
class GetPresignedPostDTO:
    filename: str


@dataclass(frozen=True)
class PresignedPostDTO:
    url: str
    key: str
    access_key_id: str
    signature: str
    policy: str


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
