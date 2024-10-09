from aiogram.fsm.state import StatesGroup, State


class AdminSearchUserSG(StatesGroup):
    SEARCH_USER = State()


class AdminWriteUserSG(StatesGroup):
    WRITE_USER = State()


class AdminUserOrdersSG(StatesGroup):
    USER_ORDERS = State()
    ONE_ORDER = State()


class MailingSG(StatesGroup):
    MESSAGE = State()
    CHECKOUT = State()


class AdminOrderLookUpSG(StatesGroup):
    START = State()
    ALL_ORDERS = State()
    PROCESSING_ORDERS = State()
    COMPLETED_ORDERS = State()
    CANCELLED_ORDERS = State()
    ORDER_INFO = State()
