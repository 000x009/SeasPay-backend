from aiogram.fsm.state import State, StatesGroup


class OrderFulfillmentSG(StatesGroup):
    ORDER_INFO = State()
    CALCULATE_COMMISSION = State()
    ATTACH_RECEIPT = State()
    PRE_CONFIRM = State()
    PRE_CONFIRM_CANCEL = State()
    CANCEL_ORDER = State()
