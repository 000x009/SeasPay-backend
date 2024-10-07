from aiogram.filters.callback_data import CallbackData


class OrderFulfillmentCallbackData(CallbackData, prefix='order_fulfillment'):
    order_id: int


class CancelOrderCallbackData(CallbackData, prefix='cancel_order'):
    order_id: int


class InformOrderIssueCallbackData(CallbackData, prefix='inform_order_issue'):
    order_id: int


class BackToOrderCallbackData(CallbackData, prefix='order'):
    order_id: int


class TakeOrderCallbackData(CallbackData, prefix='take_order'):
    order_id: int


class AdminSentMoneyCallbackData(CallbackData, prefix='money_sent'):
    order_id: int
