from aiogram.fsm.state import State, StatesGroup


class PlatformManagementSG(StatesGroup):
    PLATFORM_LIST = State()
    PLATFORM = State()
    DELETE_PLATFORM = State()

    PLATFORM_INFO = State()
    EDIT_NAME = State()
    EDIT_LOGIN_DATA = State()
    ADD_LOGIN_FIELD = State()
    EDIT_DESCRIPTION = State()
    EDIT_WEB_APP_PLACE = State()
    EDIT_IMAGE = State()

    ADD_PLATFORM_NAME = State()
    ADD_PLATFORM_DESCRIPTION = State()
    ADD_PLATFORM_LOGIN_DATA = State()
    ADD_PLATFORM_IMAGE = State()


class EditPlatformSG(StatesGroup):
    INFO = State()
    EDIT_NAME = State()
    EDIT_LOGIN_DATA = State()
    ADD_LOGIN_FIELD = State()
    EDIT_DESCRIPTION = State()
    EDIT_WEB_APP_PLACE = State()
    EDIT_IMAGE = State()


class AddPlatformSG(StatesGroup):
    NAME = State()
    DESCRIPTION = State()
    LOGIN_DATA = State()
    IMAGE = State()
