from aiogram.fsm.state import StatesGroup, State


class AdminSearchUserSG(StatesGroup):
    SEARCH_USER = State()


class AdminWriteUserSG(StatesGroup):
    WRITE_USER = State()


class AdminUserOrdersSG(StatesGroup):
    USER_ORDERS = State()
    ONE_ORDER = State()
