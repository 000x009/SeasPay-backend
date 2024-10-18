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

