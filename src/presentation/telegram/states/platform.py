from aiogram.fsm.state import State, StatesGroup


class PlatformManagementSG(StatesGroup):
    PLATFORM_LIST = State()
    PLATFORM = State()
    DELETE_PLATFORM = State()
    CREATE_PLATFORM = State()
    EDIT_LOGIN_DATA = State()
    EDIT_DATA = State()
    