from aiogram.fsm.state import State, StatesGroup


class PlatformProductManagementSG(StatesGroup):
    PRODUCT_LIST = State()
    PRODUCT = State()
    DELETE_PRODUCT = State()
    
    ADD_PRODUCT_NAME = State()
    ADD_PRODUCT_PRICE = State()
    ADD_PRODUCT_PURCHASE_URL = State()
    ADD_PRODUCT_INSTRUCTION = State()
    ADD_PRODUCT_IMAGE = State()

    EDIT_PRODUCT = State()
    EDIT_PRODUCT_NAME = State()
    EDIT_PRODUCT_PRICE = State()
    EDIT_PRODUCT_PURCHASE_URL = State()
    EDIT_PRODUCT_IMAGE = State()
    EDIT_PRODUCT_INSTRUCTION = State()
