from src.domain.exceptions.base import DomainError


class PurchaseRequestNotFound(DomainError):
    pass


class PurchaseRequestAlreadyTaken(DomainError):
    pass

