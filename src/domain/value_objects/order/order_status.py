from enum import StrEnum, auto


class OrderStatus(StrEnum):
    COMPLETE = auto()
    CANCEL = auto()
    PROCESSING = auto()
    NEW = auto()
    DELAY = auto()
