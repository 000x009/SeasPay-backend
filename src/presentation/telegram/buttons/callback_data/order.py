from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class OrderFulfillmentCallbackData(CallbackData, prefix='order_fulfillment'):
    order_id: UUID


class CancelOrderCallbackData(CallbackData, prefix='cancel_order'):
    order_id: UUID


class InformOrderIssueCallbackData(CallbackData, prefix='inform_order_issue'):
    order_id: UUID


class BackToOrderCallbackData(CallbackData, prefix='order'):
    order_id: UUID


class TakeOrderCallbackData(CallbackData, prefix='take_order'):
    order_id: UUID


class AdminSentMoneyCallbackData(CallbackData, prefix='money_sent'):
    order_id: UUID
