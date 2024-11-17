from src.domain.exceptions.base import DomainError


class UserCommissionDataError(DomainError):
    pass


class WrongCommissionError(UserCommissionDataError):
    pass


class UserCommissionNotFoundError(DomainError):
    pass
