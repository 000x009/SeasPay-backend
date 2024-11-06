from src.domain.exceptions.base import DomainError


class InvalidImageURLError(DomainError):
    pass


class InvalidProductPriceError(DomainError):
    pass


class InvalidProductNameError(DomainError):
    pass


class InvalidImageURL(DomainError):
    pass
