from aiogram.filters.callback_data import CallbackData


class ConfirmOrderCallbackData(CallbackData, prefix='confirm_order'):
    order_id: int


class CancelOrderCallbackData(CallbackData, prefix='cancel_order'):
    order_id: int
