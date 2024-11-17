from src.domain.exceptions.base import DomainError


class PlatformProductDataError(DomainError):
    pass


class InvalidImageURLError(PlatformProductDataError):
    pass


class InvalidProductPriceError(PlatformProductDataError):
    pass


class InvalidProductNameError(PlatformProductDataError):
    pass


class InvalidImageURL(PlatformProductDataError):
    pass
