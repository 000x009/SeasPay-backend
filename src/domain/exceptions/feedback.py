from src.domain.exceptions.base import DomainError


class FeedbackDataError(DomainError):
    pass


class InvalidFeedbackCommentError(FeedbackDataError):
    pass


class InvalidFeedbackStarsError(FeedbackDataError):
    pass


class FeedbackNotFoundError(DomainError):
    pass
