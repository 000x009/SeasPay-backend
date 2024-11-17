from src.domain.exceptions import DomainError


class NotAuthorizedError(DomainError):
    pass


class UserDataError(DomainError):
    pass


class EmptyValueError(UserDataError):
    pass


class UserNotFoundError(DomainError):
    pass


class WithdrawAmountError(UserDataError):
    pass
