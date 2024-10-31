from aiogram.fsm.state import StatesGroup, State


class PurchaseRequestFulfillmentSG(StatesGroup):
    REQUEST_INFO = State()
    ADD_PRICE = State()
    ADD_LOGIN_FIELDS = State()
    PRE_CONFIRM_FULFILLMENT = State()
    CONFIRM_FULFILLMENT = State()
    CANCEL_REQUEST = State()
    CANCEL_REASON = State()
