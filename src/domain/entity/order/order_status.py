from enum import Enum


class OrderStatus(Enum):
    COMPLETE = 'COMPLETE'
    CANCEL = 'CANCEL'
    WAIT = 'WAIT'
    DELAY = 'DELAY'
