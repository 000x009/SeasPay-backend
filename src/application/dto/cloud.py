from dataclasses import dataclass


@dataclass(frozen=True)
class GetPresignedURL:
    filename: str


@dataclass(frozen=True)
class PresignedURL:
    url: str
