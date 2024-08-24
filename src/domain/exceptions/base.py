from typing import Optional
from typing_extensions import Self


class DomainError(Exception):
    def __init__(self, message: Optional[str] = None):
        self.message = message


class ValueObjectError(ValueError):
    def __init__(self, message: Optional[str] = None):
        self.message = message
