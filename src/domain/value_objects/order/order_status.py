from enum import StrEnum


class OrderStatus(StrEnum):
    COMPLETE = "COMPLETE"
    CANCEL = "CANCEL"
    PROCESSING = "PROCESSING"
    NEW = "NEW"
    DELAY = "DELAY"
