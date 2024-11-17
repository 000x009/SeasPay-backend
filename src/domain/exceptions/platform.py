from src.domain.exceptions.base import DomainError


class PlatformDataError(DomainError):
    pass


class InvalidDescriptionError(PlatformDataError):
    pass


class InvalidPlatformNameError(PlatformDataError):
    pass
